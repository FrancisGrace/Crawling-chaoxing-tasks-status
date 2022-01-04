'''
Author: LinXuan
Date: 2022-01-04 01:22:05
Description: 执行爬取数据的逻辑
LastEditors: LinXuan
LastEditTime: 2022-01-04 23:31:16
FilePath: /opensource-homework/src/ObtainData/OptionData.py
'''
# TODO: 将sleep替换为等待唤醒的wait
import csv
import pprint
import time
from typing import List

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Login import login
from Task import Task

delay = 2  # 切换页面后的延迟，单位s


def get_course_list(web: Chrome) -> List[WebElement]:
    '''
        获取学生所有课程的element.仅读取在根目录的课程
    '''
    course_list = web.find_elements_by_xpath(r'/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div[3]/ul[1]/li/div[2]/h3/a')
    # 筛选可以点击的元素
    course_list = [course for course in course_list if course.is_displayed()]
    return course_list


def get_course_data(web: Chrome, course: WebElement) -> List[Task]:
    '''
        进入一门课程内获取作业的数据信息，完成后需要回退web状态
    '''
    data = list()
    course_name = course.text       # 课程名
    # 进入子页面
    # TODO: 目前只能通过点击的操作进入课程，对于文件夹内的未显示课程无能为力。
    # wait = WebDriverWait(web, 10)
    # wait.until(EC.element_to_be_clickable((By.ID, course.id)))
    course.click()
    time.sleep(delay)
    web.switch_to.window(web.window_handles[1])

    # 切换到作业界面
    homework_button: WebElement = web.find_element_by_xpath(r'/html/body/div[1]/div[3]/div[1]/div/ul[1]/li[4]/a')
    homework_button.click()

    # 回到旧版来方便快速提取信息
    web.find_element_by_xpath("/html/body/div[1]/div[1]/div/a").click()

    # 获取所有任务的元素列表
    task_list: List[WebElement] \
        = web.find_elements_by_xpath("/html/body/div[3]/div[1]/div/div/div/div[2]/ul/li")
    for task in task_list:
        task_data = get_task_data(task, course_name)
        data.append(task_data)

    # 恢复web状态
    web.close()
    web.switch_to.window(web.window_handles[0])
    print("debug: ", course_name, ": over")
    return data


def get_task_data(task: WebElement, course_name) -> Task:
    task_data = Task(course_name)
    task_name = task.find_element_by_tag_name("a").text
    spans = task.find_elements_by_xpath("div/span")
    start = spans[0].text.split("\n")[1]
    end = spans[1].text.split("\n")[1]
    status = spans[2].text.split("\n")[1]
    score = spans[3].text
    task_data.full(task_name=task_name, start=start, end=end, status=status, score=score)
    return task_data


def obtain_data(user_data, url) -> List[Task]:
    ops = Options()
    ops.add_argument(f'user-data-dir={user_data}')
    ops.add_argument("--headless")
    ops.add_argument("--disable-gpu")
    # 下面两个参数视图解决无头状态下最后一个元素不可点击的问题。
    # 有头状态下似乎工作正常，原因暂时不明。猜测可能由于浏览器界面大小不同是展开的元素数量不同有关。
    ops.add_argument("--window-size=1920,1080")
    ops.add_argument("--start-maximized")
    web = Chrome(options=ops)
    # 展开页面
    web.get(url)
    time.sleep(delay)
    web.implicitly_wait(4)
    # 获取课程列表
    course_list = get_course_list(web)

    data_group = list()
    # 爬取对应课程数据
    for course in course_list:
        data = get_course_data(web, course)
        data_group.extend(data)

    pprint.pprint(data_group)
    return data_group


def save_to_csv(data_group: List[Task], filename):
    '''
        数据保存到csv文件中
    '''
    with open(filename, mode='w', encoding='utf-8') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(["course_name", "task_name", "start", "end", "status", "score"])
        for task in data_group:
            csvwriter.writerow(task.to_data())
    pass


def main():
    # 登陆
    user_data = '/resource/user-data'[1:]
    url = "https://mooc2-ans.chaoxing.com/visit/interaction"
    login(user_data=user_data, url=url)

    # 爬取数据
    data_group = obtain_data(user_data, url)
    save_to_csv(data_group, "/resource/data.csv"[1:])
    pass


if __name__ == "__main__":
    main()

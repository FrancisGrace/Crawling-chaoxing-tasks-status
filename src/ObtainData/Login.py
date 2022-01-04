'''
Author: LinXuan
Date: 2022-01-04 00:06:50
Description: 引导进行登陆
LastEditors: LinXuan
LastEditTime: 2022-01-04 15:04:32
FilePath: /opensource-homework/src/ObtainData/Login.py
'''
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from typing import *
import os
import time


def login(user_data: str, url: str):
    def get_options(user_data):
        ops = Options()
        if os.path.exists(user_data) == False:
            os.mkdir(user_data)
        ops.add_argument(f'user-data-dir={user_data}')
        return ops

    # user_data = r'/resource/user-data'[1:]
    # url = "https://mooc2-ans.chaoxing.com/visit/interaction"
    web = Chrome(options=get_options(user_data))
    web.get(url)
    print("请在弹出的窗口内登陆。登陆后关闭浏览器")
    while True:
        # 检测到浏览器关闭后退出
        try:
            web.window_handles
            time.sleep(2)
        except:
            print("浏览器已关闭")
            break


def main():
    user_data = "tmp-data"
    login(user_data)
    print("over")
    pass


if __name__ == "__main__":
    main()

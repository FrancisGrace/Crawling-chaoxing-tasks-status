from os import system
import csv
import matplotlib.pyplot as plt
from prettytable import PrettyTable, prettytable
from datetime import datetime


def display_table():
    # 创建表格
    table = PrettyTable(['科目', '作业名称', '截止时间', '剩余时间'])
    table.set_style(prettytable.PLAIN_COLUMNS)
    with open('data.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['status'] != '已完成':
                end_date = datetime.fromisoformat(row['end'])
                now_date = datetime.now()
                delta_date = end_date - now_date
                delta = '{}天{}小时'.format(delta_date.days, delta_date.seconds // 3600)
                table.add_row([row['name'], row['name'], row['end'], delta])
    print(table)


def display_chart():
    # 图表
    plt.rcParams['font.sans-serif'] = ['STZhongSong']  # 用来正常显示中文标签
    # plt.rcParams['font.size'] = '16'
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.gcf().subplots_adjust(bottom=0.15, wspace=0.5)
    # TODO 循环遍历有已批作业的科目
    plt.subplot(2, 2, 1)
    plt.xlabel('作业名称')
    plt.ylabel('分数')

    # TODO 获取作业成绩
    hw_subject = '模拟与数字电路'
    hw_list = ['第一周作业', '第二周作业', '第三周作业', '第四周作业']
    hw_score = [100, 100, 95, 100]
    plt.title(hw_subject + '历次作业成绩', fontsize='12')
    plt.bar(range(4), hw_score, align='center', color='steelblue')  # 绘制条形图
    plt.xticks(range(4), hw_list, rotation=-30)  # 设置横轴标签

    for x, y in enumerate(hw_score):
        plt.text(x, y, y, ha='center')  # 在图中标注数字
    # TODO 循环结束

    plt.show()


def main():
    display_table()
    display_chart()
    system('pause')


if __name__ == "__main__":
    main()

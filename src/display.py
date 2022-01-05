'''
Author: FrancisGrace
Date: 2021-12-31 09:50:22
Description: 显示可修改作业的截止时间和已批改作业的成绩
LastEditors: FrancisGrace
LastEditTime: 2022-01-05 09:04:54
FilePath: /Crawling-chaoxing-tasks-status/src/display.py
'''
from os import system
import csv
import matplotlib.pyplot as plt
from prettytable import PrettyTable, prettytable
from datetime import datetime


def display_table():
    """
    将未提交或可修改的作业以表格形式显示
    """
    # 创建表格
    table = PrettyTable(['科目', '作业名称', '截止时间', '剩余时间', '是否已提交'])
    table.set_style(prettytable.PLAIN_COLUMNS)
    # 读取信息
    with open('../resource/data.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['status'] != '已完成':
                end_date = datetime.fromisoformat(row['end'])
                now_date = datetime.now()
                delta_date = end_date - now_date
                delta = '{}天{}小时'.format(delta_date.days, delta_date.seconds // 3600)
                status = '是' if row['status'] == '待批阅' else '否'
                table.add_row([row['course_name'], row['task_name'], row['end'], delta, status])
    print(table)


def display_chart():
    """
    将已批改的作业以统计图形式显示
    """
    # 设置图表
    plt.rcParams['font.sans-serif'] = ['STZhongSong']  # 用来正常显示中文标签
    # plt.rcParams['font.size'] = '16'
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.gcf().subplots_adjust(left=0.4, bottom=0.15, wspace=0.5, hspace=0.5)
    plt.tight_layout()
    subjects = []
    # 读取科目
    with open('../resource/data.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['score'] != '':
                try:
                    subjects.index(row['course_name'])
                except ValueError:
                    subjects.append(row['course_name'])
    # 读取各科作业成绩并绘制
    for i in range(0, len(subjects)):
        plt.subplot(2, (len(subjects) + 1) // 2, i + 1)
        plt.ylabel('作业名称')
        plt.xlabel('分数')
        hw_subject = subjects[i]
        hw_list = []
        hw_score = []
        with open('../resource/data.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['course_name'] == subjects[i] and row['score'] != '':
                    hw_list.append(row['task_name'])
                    hw_score.append(float(row['score'][:-1]))
        plt.title(hw_subject + '历次作业成绩', fontsize='12')
        plt.barh(range(len(hw_score)), hw_score, align='center', color='steelblue')  # 绘制条形图
        plt.yticks(range(len(hw_list)), hw_list)  # 设置横轴标签

        for x, y in enumerate(hw_score):
            plt.text(y, x - 0.2, y, ha='right')  # 在图中标注数字
    # 显示图表
    plt.show()


def main():
    display_table()
    display_chart()
    system('pause')


if __name__ == "__main__":
    main()

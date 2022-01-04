'''
Author: LinXuan
Date: 2022-01-03 23:37:40
Description: 储存任务的格式
LastEditors: LinXuan
LastEditTime: 2022-01-04 23:12:50
FilePath: /opensource-homework/src/ObtainData/Task.py
'''
from datetime import datetime


class Task:
    def __init__(self, course) -> None:
        self.course = course
        self.task_name = ""
        self.start_time = ""
        self.end_time = ""
        self.status = ""
        self.score = None
        pass

    def full(self, task_name, start, end, status, score=None):
        self.task_name = task_name
        self.start_time = start
        self.end_time = end
        self.status = status
        self.score = score
        pass

    def to_data(self):
        return (
            self.course,
            self.task_name,
            self.start_time,
            self.end_time,
            self.status,
            self.score
        )

    def __repr__(self) -> str:
        return self.to_data().__repr__()


def main():
    tmp = Task("编译原理")
    tmp.full("任务一", "2021-12-20 14:02", "2021-12-29 18:00", "已完成", 5)
    print(tmp.to_data())
    pass


if __name__ == "__main__":
    main()

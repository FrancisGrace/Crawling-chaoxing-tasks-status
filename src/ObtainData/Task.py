'''
Author: LinXuan
Date: 2022-01-03 23:37:40
Description: 储存任务的格式
LastEditors: LinXuan
LastEditTime: 2022-01-04 00:05:33
FilePath: /opensource-homework/src/ObtainData/task.py
'''
from datetime import datetime


class Task:
    def __init__(self, course) -> None:
        self.course = course
        self.start_time = ""
        self.end_time = ""
        self.status = ""
        self.score = None
        pass

    def full(self, start, end, status, score=None):
        self.start_time = start
        self.end_time = end
        self.status = status
        self.score = score
        pass

    def to_data(self):
        return (
            self.course,
            self.start_time,
            self.end_time,
            self.status,
            self.score
        )

    def __repr__(self) -> str:
        return self.to_data().__repr__()


def main():
    tmp = Task("编译原理")
    tmp.full("2021-12-20 14:02", "2021-12-29 18:00", "已完成", 5)
    print(tmp.to_data())
    pass


if __name__ == "__main__":
    main()

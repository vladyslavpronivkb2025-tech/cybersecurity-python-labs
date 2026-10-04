import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from laba1.task1 import run_task1
from laba1.task2 import run_task2
from laba1.task3 import run_task3


def main():
    print("\n>>> ЗАПУСК ЛАБОРАТОРНОЇ РОБОТИ №1 <<<\n")
    run_task1()
    run_task2()
    run_task3()
    print(">>> ВСІ ЗАВДАННЯ ВИКОНАНО УСПІШНО! <<<\n")


if __name__ == "__main__":
    main()

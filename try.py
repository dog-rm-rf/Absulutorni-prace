# class All_tasks:
#     def __init__(self):
#         self.vector_of_all_tasks_objects = []

# # Create two different objects
# tasks1 = All_tasks()
# tasks2 = All_tasks()

# # Add something to the first object's list
# tasks1.vector_of_all_tasks_objects.append("Task A")

# # Now check what's in the second object's list
# print("tasks1 list:", tasks1.vector_of_all_tasks_objects)
# print("tasks2 list:", tasks2.vector_of_all_tasks_objects)

# my_list = ["apple", "banana",  "orange","banana"]
# my_list.remove("banana")
# print(my_list)
# class Task:
#     def __init__(self, name, date):
#         self.name = name
#         self.date = date

# task1 = Task("homework", "today")
# task2 = Task("homework", "today")  # Same content, different object
# my_tasks = [task1, task2]
# my_tasks.remove(task1)


# -*- coding: utf-8 -*-
import sqlite3
import sys
import io
import os
from datetime import datetime 
import pandas as pd

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path


list_of_all_goals_objects = [["goal1", "goal2", "goal3"], ["goal4", "goal5", "goal6"]]

# for x in list_of_all_goals_objects:
#     print(f"Your goals for your 12 weeks are {x[0]}\n")


def add_addiction_into_copy(whole_addiction, y_n):
        list_of_all_goals_objects.append(whole_addiction)
        list_of_all_goals_objects[-1][1] = y_n
        return list_of_all_goals_objects
        


result = add_addiction_into_copy(["gaminig", None, "Nov 6"], "y")
print(result)

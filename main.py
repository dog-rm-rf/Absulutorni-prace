# -*- coding: utf-8 -*-
import sqlite3
import sys
import io
from datetime import datetime 
from models.task import Task
from models.all_tasks import All_tasks

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')
# global variables
nAll_tasks = All_tasks()
output = None
print("Hello welcome to 12 week app")
while (output != 0):
    
    print("If you want add task press 1\n" + 
            "if you want remove press 2\n" +
            "if you want to see all tasks press 3\n" +
            "if you want quit press q")
    answer = input()
    match answer:
            # add
        case "1":
            print("give name to task:")
            task_name = input()
            print("give me date:")
            date = input()
            p1 = Task(task_name, date)
            nAll_tasks.add_new_task(p1)
            #remove
        case "2":
            print("which task you want to remove\n type name of task")
            task_remove_name = input()
            for x in nAll_tasks.vector_of_all_tasks_objects:
                if(x.name == task_remove_name): #object is type Task so task have name and date
                    nAll_tasks.vector_of_all_tasks_objects.remove(x)
                    break
        case "3":
            nAll_tasks.show_all_tasks()
        case "q":
            output = 0
        case _:
            print("The language doesn't matter, what matters is solving problems.")


# class nProgram:
#     def __init__(self):
#         pass
# class stats: # completed 3/5 after evalution of ratings
#     def __init__(self):
#         pass
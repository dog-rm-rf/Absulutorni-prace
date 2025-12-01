# -*- coding: utf-8 -*-
import sys
import io
#import mysql.connector
from datetime import datetime 
#from models.task import Task
from models.all_tasks import All_tasks
from models.GUI import GUI
from models.goal import Goal
from models.addiction import Addiction
from models.filters import Filter
from models.notes_class import Note
from models.reward import Reward


# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')

#Create connection
# connection = mysql.connector.connect(
#     host='localhost',        # MySQL is running on your PC
#     user='your_username',    # MySQL user account
#     password='your_password', # MySQL password
#     database='task_manager'  # Name of your database
# )

# cursor = connection.cursor()  # This lets you send SQL commands




# global variables
nAll_tasks = All_tasks()
nAddiction = Addiction()
nNote = Note()
nReward = Reward()
goal = Goal(nAll_tasks)
nFilter = Filter(nAll_tasks)

GUI = GUI(nAll_tasks, goal, nAddiction, nNote, nReward, nFilter)
GUI.menu()



# class nProgram:
#     def __init__(self):
#         pass
# class stats: # completed 3/5 after evalution of ratings
#     def __init__(self):
#         pass
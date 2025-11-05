# -*- coding: utf-8 -*-
import sqlite3
import sys
import io
import os
from datetime import datetime 
import pandas as pd

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')

class All_tasks:
    #
    def __init__(self):
        self.file_data_frame = "tasks_dataframe.pkl"
        if os.path.exists(self.file_data_frame):
            self.data_frame = pd.read_pickle(self.file_data_frame)
            self.list_of_all_tasks_objects = self.data_frame.values.tolist()
        else:
            self.data_frame = pd.DataFrame()
            self.list_of_all_tasks_objects = []

    def add_new_task(self, task):
        self.list_of_all_tasks_objects.append(task)
        self.update_data_frame()
        
    def update_data_frame(self):
        self.data_frame = pd.DataFrame(self.list_of_all_tasks_objects, columns=["activity", "date", "desired_time_spent_hours", "score", "review"])
        self.data_frame.to_pickle(self.file_data_frame)

    def remove_task_df(self, taskIndex):
        del self.list_of_all_tasks_objects[taskIndex]
        self.update_data_frame()

    def save_data_frame(self):
        self.data_frame.to_pickle(self.file_data_frame)
        
    def add_score_to_task(self, index, score, learnt, dont_undersand, next_step): #3 je pozice score
        self.list_of_all_tasks_objects[index][3] = score
        self.list_of_all_tasks_objects[index][4][0] = learnt
        self.list_of_all_tasks_objects[index][4][1] = dont_undersand
        self.list_of_all_tasks_objects[index][4][2] = next_step
        self.update_data_frame()
        




    # def readDataFrame(self):
    #     self.data_frame = pd.read_csv(self.file_data_frame)
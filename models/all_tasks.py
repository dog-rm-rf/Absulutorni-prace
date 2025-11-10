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
        self.file_data_frame_task = "tasks_dataframe.pkl"
        if os.path.exists(self.file_data_frame_task):
            self.data_frame = pd.read_pickle(self.file_data_frame_task)
            self.list_of_all_tasks_objects = self.data_frame.values.tolist()
        else:
            self.data_frame = pd.DataFrame()
            self.list_of_all_tasks_objects = []

    def add_new_task(self, task):
        self.list_of_all_tasks_objects.append(task)
        self.update_data_frame()
    
    def setting_task(self, index, score, learnt, dont_understand, next_step):
        self.list_of_all_tasks_objects[index][3] = score
        self.list_of_all_tasks_objects[index][4][0] = learnt
        self.list_of_all_tasks_objects[index][4][1] = dont_understand
        self.list_of_all_tasks_objects[index][4][2] = next_step
        self.update_data_frame()   
        
    def update_data_frame(self):
        self.data_frame = pd.DataFrame(self.list_of_all_tasks_objects, columns=["activity", "task_sub_class", "date", "desired_time_spent_hours", "score", "review"])
        self.data_frame.to_pickle(self.file_data_frame_task)

    def remove_task_df(self, taskIndex):
        del self.list_of_all_tasks_objects[taskIndex]
        self.update_data_frame()

    def save_data_frame(self):
        self.data_frame.to_pickle(self.file_data_frame_task)
        
    def delete_column(self):
        if 'addiction' in self.data_frame.columns:
            self.data_frame = self.data_frame.drop(columns=['addiction'])
            # Optional: update the list to stay in sync
            self.list_of_all_tasks_objects = self.data_frame.values.tolist()
        else:
            print("Column 'addiction' not found.")
            
    # def add_column(self):
    #     self.data_frame = self.data_frame(columns=['activity', 'date', 'score'])
    
        
    # def readDataFrame(self):
    #     self.data_frame = pd.read_csv(self.file_data_frame)
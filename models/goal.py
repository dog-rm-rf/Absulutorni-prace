# -*- coding: utf-8 -*-
import sqlite3
import sys
import io
import os
from datetime import datetime 
import pandas as pd

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')


class Goal:
    def __init__(self):
        self.file_data_frame_goal = "goals_dataframe.pkl"
        if os.path.exists(self.file_data_frame_goal):
            self.data_frame = pd.read_pickle(self.file_data_frame_goal)
            self.list_of_all_goals_objects = self.data_frame.values.tolist()
        else:
            self.data_frame = pd.DataFrame()
            self.list_of_all_goals_objects = []

    def add_goal(self, goal, time_input, avrage_score ):
        self.list_of_all_goals_objects.append(goal)
        self.list_of_all_goals_objects.append(time_input)
        self.list_of_all_goals_objects.append(avrage_score)
        self.update_df_goals()
        
    def update_df_goals(self,):
        self.data_frame = pd.DataFrame(self.list_of_all_goals_objects, columns=["goal_name", "timer", "avrage_score"])
        self.data_frame.to_pickle(self.file_data_frame_goal)
    
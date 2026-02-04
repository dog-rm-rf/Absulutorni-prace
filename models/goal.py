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
    def __init__(self, allTask):
        # Vytvoř data složku pokud neexistuje
        os.makedirs("data", exist_ok=True)
        self.allTask = allTask
        self.file_data_frame_goal = "data/goals_dataframe.pkl"
        if os.path.exists(self.file_data_frame_goal):
            self.goals_dataframe = "data/active/goals_dataframe.pkl"  # ← ZMĚNA
            self.list_of_all_goals_objects = self.data_frame.values.tolist()
        else:
            self.data_frame = pd.DataFrame()
            self.list_of_all_goals_objects = []

    def add_goal(self, goal):
        self.list_of_all_goals_objects.append(goal)
        self.update_df_goals()
        
    def update_df_goals(self):
        self.data_frame = pd.DataFrame(self.list_of_all_goals_objects, columns=[
        "goal_name",        # 0
        "subclass",         # 1
        "timer",            # 2 - kolik hodin chceš strávit
        "average_score",    # 3 - jaké průměrné score chceš
        "date_of_creation", # 4 - začátek cyklu (start_date)
        "checked",          # 5 - splněno/nesplněno (bool)
        "end_date",         # 6 - konec cyklu
        "completed"         # 7 - cyklus dokončen (bool)
    ]
        )
        self.data_frame.to_pickle(self.file_data_frame_goal)
    
    def upadating_timer(self, index1, value):
        for x in self.list_of_all_goals_objects:
            if self.allTask.list_of_all_tasks_objects[index1][1] == x[1]:
                x[2] -= value
                self.update_df_goals()
                
    def removing_timer(self, goalIndex):
        del self.list_of_all_goals_objects[goalIndex]
        self.update_df_goals()
        
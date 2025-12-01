# -*- coding: utf-8 -*-
import sqlite3
import sys
import io
import os
from datetime import datetime 
import pandas as pd

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')

class Reward:
    def __init__(self):
        self.file_data_frame_reward = "reward_dataframe.pkl"
        if os.path.exists(self.file_data_frame_reward):
            self.data_frame = pd.read_pickle(self.file_data_frame_reward)
            self.list_of_all_reward_objects = self.data_frame.values.tolist()
        else:
            self.data_frame = pd.DataFrame()
            self.list_of_all_reward_objects = []
            
    def add_reward(self, reward):
        self.list_of_all_reward_objects.append(reward)
        self.update_df_rewards()
        
    def update_df_rewards(self):
        self.data_frame = pd.DataFrame(self.list_of_all_reward_objects, columns=["date_of_creation", "reward_name", "time", "finished"])
        self.data_frame.to_pickle(self.file_data_frame_reward)
        
    
# -*- coding: utf-8 -*-
import sqlite3
import sys
import io
import os
from datetime import datetime 
import pandas as pd

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')

class Addiction:
    def __init__(self):
        self.file_data_frame_addiction_original = "addiction_dataframe_original.pkl"
        self.file_data_frame_addiction_copy = "addiction_dataframe_copies.pkl"
        #original
        if os.path.exists(self.file_data_frame_addiction_original):
            self.data_frame_original = pd.read_pickle(self.file_data_frame_addiction_original)
            self.list_of_all_addiction_objects_original = self.data_frame_original.values.tolist()
        else:
            self.data_frame_original = pd.DataFrame()
            self.list_of_all_addiction_objects_original = []
        #copies
        if os.path.exists(self.file_data_frame_addiction_copy):
            self.data_frame_copy = pd.read_pickle(self.file_data_frame_addiction_copy)
            self.list_of_all_addiction_objects_copy = self.data_frame_copy.values.tolist()
        else:
            self.data_frame_copy = pd.DataFrame()
            self.list_of_all_addiction_objects_copy = []
        
        
        
    def add_addiction_into_original(self, addiction):
        self.list_of_all_addiction_objects_original.append(addiction)
        self.update_df_addiction_original()

    def add_addiction_into_copy(self, whole_addiction, y_n):
        self.list_of_all_addiction_objects_copy.append(whole_addiction)
        self.list_of_all_addiction_objects_copy[-1][2] = y_n
        self.update_df_addiction_copy()

        #date shouold be there just to track when it started, but i want to not show the date in gui
    
    def update_df_addiction_original(self):
        self.data_frame_original = pd.DataFrame(self.list_of_all_addiction_objects_original, columns=["addiction name", "date_it_started", "did you manage to survive the day without the addiction"])
        self.data_frame_original.to_pickle(self.file_data_frame_addiction_original)

    def update_df_addiction_copy(self):
        self.data_frame_copy = pd.DataFrame(self.list_of_all_addiction_objects_copy, columns=["addiction name", "date_it_started", "did you manage to survive the day without the addiction"])
        self.data_frame_copy.to_pickle(self.file_data_frame_addiction_copy)


    def show_addiction(self):
        for x in self.list_of_all_addiction_objects_original:
            print(x)
    def show_copies(self):
        for x in self.list_of_all_addiction_objects_copy:
            print(x)
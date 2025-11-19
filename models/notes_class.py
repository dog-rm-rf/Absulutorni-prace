# -*- coding: utf-8 -*-
import sqlite3
import sys
import io
import os
from datetime import datetime 
import pandas as pd

import time

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')

class Note:
    def __init__(self):
        self.notes_file = "notes_file.pkl"
        if os.path.exists(self.notes_file):
            self.data_frame = pd.read_pickle(self.notes_file)
            self.list_of_all_notes_objects = self.data_frame.values.tolist()
        else:
            self.data_frame = pd.DataFrame()
            self.list_of_all_notes_objects = []

    def create_note(self, note):# date, subclass, topic, text):
        self.list_of_all_notes_objects.append(note)
        self.update_df_note()


    def update_df_note(self):
        

        self.data_frame = pd.DataFrame(self.list_of_all_notes_objects, columns=["date", "subclass", "topic", "text"])
        self.data_frame.to_pickle(self.notes_file)

# start_time = time.time()
# end_time = time.time()
# print(f"Time taken: {end_time - start_time:.4f} seconds")


        
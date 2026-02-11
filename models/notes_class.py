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
        """
        Inicializace Note - načte notes ze souboru
        """
        # Nastavení cesty
        self.notes_file = "data/active/notes_file.pkl"
        
        # Vytvoř složku pokud neexistuje
        os.makedirs("data/active", exist_ok=True)
        
        # Načti data ze souboru
        if os.path.exists(self.notes_file):
            # Soubor existuje - načti ho
            self.data_frame = pd.read_pickle(self.notes_file)  # ← PŘIDEJ!
            self.list_of_all_notes_objects = self.data_frame.values.tolist()
            print(f"✅ Načteno {len(self.list_of_all_notes_objects)} notes")
        else:
            # Soubor neexistuje - vytvoř prázdný DataFrame
            print("⚠️ Notes soubor neexistuje - vytváření prázdného")
            self.data_frame = pd.DataFrame(columns=["date", "subclass", "topic", "text"])
            self.list_of_all_notes_objects = []
            
            # Ulož prázdný soubor
            self.update_data_frame()

    def create_note(self, note):# date, subclass, topic, text):
        self.list_of_all_notes_objects.append(note)
        self.update_data_frame()


    def update_data_frame(self):
        

        self.data_frame = pd.DataFrame(self.list_of_all_notes_objects, columns=["date", "subclass", "topic", "text"])
        self.data_frame.to_pickle(self.notes_file)

# start_time = time.time()
# end_time = time.time()
# print(f"Time taken: {end_time - start_time:.4f} seconds")


        
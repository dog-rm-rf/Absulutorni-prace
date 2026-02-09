# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime
import pandas as pd

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')

class Settings:
    def __init__(self):
        # Vytvoř data složku pokud neexistuje
        os.makedirs("data/active", exist_ok=True)
        self.file_settings = "data/active/settings_dataframe.pkl"  # ← ZMĚNA
        self.load_settings()
    
    def load_settings(self):
        """Načte nastavení ze souboru, nebo vytvoří výchozí"""
        if os.path.exists(self.file_settings):
            # Soubor existuje - načti data
            self.data_frame = pd.read_pickle(self.file_settings)
            self.settings_list = self.data_frame.values.tolist()
            
            # settings_list[0] = [start_date_string, goals_set_bool]
            # Index 0: start_date (string)
            # Index 1: goals_set (bool)
            #fromisoformat do datetime formatu
            self.start_date = datetime.fromisoformat(self.settings_list[0][0])
            self.goals_set = self.settings_list[0][1]
        else:
            # První spuštění - žádný soubor neexistuje
            self.start_date = None
            self.goals_set = False
            self.settings_list = []
    
    def set_goals_completed(self, value=True):
        """Označí že goals byly nastaveny"""
        self.goals_set = value
        self.save_settings()
    
    def save_settings(self):
        """Uloží nastavení do pickle souboru"""
        # [start_date_string, goals_set_bool]
        self.settings_list = [[self.start_date.isoformat(), self.goals_set]]
        self.data_frame = pd.DataFrame(self.settings_list, columns=['start_date', 'goals_set'])
        self.data_frame.to_pickle(self.file_settings)
    
    

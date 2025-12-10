# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime
import pandas as pd

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')

class Settings:
    def __init__(self):
        self.file_settings = "settings_dataframe.pkl"
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
    
    def is_first_login(self):
        """Kontrola jestli je první přihlášení"""
        return self.start_date is None
    
    def set_start_date(self, date):
        """Nastaví start datum (první přihlášení)"""
        self.start_date = date
        self.save_settings()
    
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
    
    def calculate_current_week(self):
        """Spočítá aktuální týden od start_date"""
        if self.start_date is None:
            return 1
        
        today = datetime.now()
        days_since_start = (today - self.start_date).days
        week = (days_since_start // 7) + 1
        
        # Omezení na 1-12
        if week < 1:
            week = 1
        elif week > 12:
            week = 12
        
        return week
    
    def needs_new_cycle(self):
        """Kontrola jestli uplynulo 12 týdnů (potřeba nový cyklus)"""
        if self.start_date is None:
            return False
        
        today = datetime.now()
        days_since_start = (today - self.start_date).days
        return days_since_start >= (12 * 7)  # 84 dní
    
    def get_start_weekday(self):
        """Vrátí den v týdnu kdy začal cyklus (0=Mon, 6=Sun)"""
        if self.start_date is None:
            return 0  # Default Monday
        return self.start_date.weekday()
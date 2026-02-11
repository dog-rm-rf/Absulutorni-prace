# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')


class Settings:
    def __init__(self):
        # Vytvoř data složku pokud neexistuje
        os.makedirs("data/active", exist_ok=True)
        
        self.file_settings = "data/active/settings_dataframe.pkl"
        self.goals_set = False  # Výchozí hodnota
        
        self.load_settings()
    
    def load_settings(self):
        """Načte nastavení ze souboru, nebo vytvoří výchozí"""
        if os.path.exists(self.file_settings):
            # Soubor existuje - načti data
            self.data_frame = pd.read_pickle(self.file_settings)
            
            if not self.data_frame.empty:
                # Načti goals_set (první sloupec)
                self.goals_set = self.data_frame.iloc[0, 0]
                print(f"✅ Settings načteny: goals_set = {self.goals_set}")
        else:
            # První spuštění - žádný soubor neexistuje
            print("⚠️ Settings neexistují - vytváření nových")
            self.goals_set = False
            self.save_settings()
    
    def set_goals_completed(self, value=True):
        """Označí že goals byly nastaveny"""
        self.goals_set = value
        self.save_settings()
        print(f"✅ Goals completed nastaveno na: {value}")
    
    def save_settings(self):
        """Uloží nastavení do pickle souboru"""
        # DataFrame s jediným sloupcem: goals_set
        self.data_frame = pd.DataFrame([[self.goals_set]], columns=['goals_set'])
        self.data_frame.to_pickle(self.file_settings)
        print(f"✅ Settings uloženy: goals_set = {self.goals_set}")
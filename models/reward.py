# -*- coding: utf-8 -*-
import sys
import os
from datetime import datetime 
import pandas as pd

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')


class Reward:
    def __init__(self):
        """
        Inicializace Reward - načte rewards ze souboru
        """
        # Nastavení cesty
        self.reward_dataframe = "data/active/reward_dataframe.pkl"
        
        # Vytvoř složku pokud neexistuje
        os.makedirs("data/active", exist_ok=True)
        
        # Načti data ze souboru
        if os.path.exists(self.reward_dataframe):
            # Soubor existuje - načti ho
            self.data_frame = pd.read_pickle(self.reward_dataframe)
            self.list_of_all_reward_objects = self.data_frame.values.tolist()
            print(f"✅ Načteno {len(self.list_of_all_reward_objects)} rewards")

            # ===== MIGRACE - PŘIDEJ actual_time KE STARÝM REWARDS =====
            migrated = False
            for reward in self.list_of_all_reward_objects:
                if len(reward) == 4:  # Starý formát
                    # Přidej actual_time = plánovaný čas (default)
                    reward.append(reward[2])  # actual_time = time
                    migrated = True
            
            if migrated:
                print(f"🔄 Migrace {len(self.list_of_all_reward_objects)} rewards - přidán sloupec actual_time")
                self.update_data_frame()  # Ulož migrovaná data
            # ===== KONEC MIGRACE =====

        else:
            # Soubor neexistuje - vytvoř prázdný DataFrame
            print("⚠️ Rewards soubor neexistuje - vytváření prázdného")
            self.data_frame = pd.DataFrame(columns=["date", "name", "time", "finished", "actual_time"])
            self.list_of_all_reward_objects = []
            
            # Ulož prázdný soubor
            self.update_data_frame()
    
    def add_reward(self, reward):
        """
        Přidá novou reward do listu a uloží
        
        Args:
            reward: [date, name, time, finished]
        """
        self.list_of_all_reward_objects.append(reward)
        self.update_data_frame()
    
    def update_data_frame(self):
        """
        Uloží list zpět do DataFrame a uloží do pickle souboru
        """
        self.data_frame = pd.DataFrame(self.list_of_all_reward_objects, 
                                       columns=["date", "name", "time", "finished"])
        self.data_frame.to_pickle(self.reward_dataframe)
        
    
# -*- coding: utf-8 -*-
import sys
import os
from datetime import datetime 
import pandas as pd

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')


class Goal:
    def __init__(self, allTask):
        """
        Inicializace Goal - načte goals ze souboru
        
        Args:
            allTask: Instance All_tasks třídy
        """
        self.allTask = allTask
        
        # Nastavení cesty
        self.goals_dataframe = "data/active/goals_dataframe.pkl"
        
        # Vytvoř složku pokud neexistuje
        os.makedirs("data/active", exist_ok=True)
        
        # Načti data ze souboru
        if os.path.exists(self.goals_dataframe):
            # Soubor existuje - načti ho
            self.data_frame = pd.read_pickle(self.goals_dataframe)
            self.list_of_all_goals_objects = self.data_frame.values.tolist()
            print(f"✅ Načteno {len(self.list_of_all_goals_objects)} goals")
        else:
            # Soubor neexistuje - vytvoř prázdný DataFrame
            print("⚠️ Goals soubor neexistuje - vytváření prázdného")
            self.data_frame = pd.DataFrame(columns=[
                "goal_name",        # 0
                "subclass",         # 1
                "timer",            # 2 - kolik hodin chceš strávit
                "average_score",    # 3 - jaké průměrné score chceš
                "date_of_creation", # 4 - začátek cyklu (start_date)
                "checked",          # 5 - splněno/nesplněno (bool)
                "end_date",         # 6 - konec cyklu
                "completed"         # 7 - cyklus dokončen (bool)
            ])
            self.list_of_all_goals_objects = []
            
            # Ulož prázdný soubor
            self.update_data_frame()
    
    def add_goal(self, goal):
        """
        Přidá nový goal do listu a uloží
        
        Args:
            goal: [goal_name, subclass, timer, avg_score, date_creation, checked, end_date, completed]
        """
        self.list_of_all_goals_objects.append(goal)
        self.update_data_frame()
    
    def update_data_frame(self):
        """
        Uloží list zpět do DataFrame a uloží do pickle souboru
        """
        self.data_frame = pd.DataFrame(self.list_of_all_goals_objects, columns=[
            "goal_name",        # 0
            "subclass",         # 1
            "timer",            # 2 - kolik hodin chceš strávit
            "average_score",    # 3 - jaké průměrné score chceš
            "date_of_creation", # 4 - začátek cyklu (start_date)
            "checked",          # 5 - splněno/nesplněno (bool)
            "end_date",         # 6 - konec cyklu
            "completed"         # 7 - cyklus dokončen (bool)
        ])
        self.data_frame.to_pickle(self.goals_dataframe)
    
    def upadating_timer(self, index1, value):
        """
        Aktualizuje timer goalu na základě tasku
        
        Args:
            index1: Index tasku
            value: Hodnota k odečtení
        """
        for x in self.list_of_all_goals_objects:
            if self.allTask.list_of_all_tasks_objects[index1][1] == x[1]:
                x[2] -= value
        self.update_data_frame()
    
    def removing_timer(self, goalIndex):
        """
        Smaže goal
        
        Args:
            goalIndex: Index goalu ke smazání
        """
        del self.list_of_all_goals_objects[goalIndex]
        self.update_data_frame()
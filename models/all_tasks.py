# -*- coding: utf-8 -*-
import sqlite3
import sys
import io
import os
from datetime import datetime 
import pandas as pd

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')

class All_tasks:

    def __init__(self):
        self.pathToDataFrame = "tasks_dataframe"
        if os.path.exists(self.pathToDataFrame):
            self.tasks_dataframe = pd.read_pickle(self.pathToDataFrame)
            self.list_of_all_tasks_objects = self.tasks_dataframe.values.tolist()
        else:
            self.tasks_dataframe = pd.DataFrame()
            self.list_of_all_tasks_objects = []

    # @staticmethod
    def add_new_task(self, task):
        self.list_of_all_tasks_objects.append(task)
        self.updateDataFrame()
        
    def updateDataFrame(self):
        self.tasks_dataframe = pd.DataFrame(self.list_of_all_tasks_objects, columns=["activity", "date"])
        self.tasks_dataframe.to_pickle(self.pathToDataFrame)

    def removeTask(self, taskIndex):
        del self.list_of_all_tasks_objects[taskIndex]
        self.updateDataFrame()

    def saveDataFrame(self):
        self.tasks_dataframe.to_pickle(self.pathToDataFrame)

    # def readDataFrame(self):
    #     self.tasks_dataframe = pd.read_csv(self.pathToDataFrame)
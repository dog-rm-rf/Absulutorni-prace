# -*- coding: utf-8 -*-
import sqlite3
import sys
import io
from datetime import datetime 

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')

class All_tasks:

    vector_of_all_tasks_objects = []

    # @staticmethod
    def add_new_task(self, object):
        self.vector_of_all_tasks_objects.append(object)

    def remove_task(self, object):
        self.vector_of_all_tasks_objects.pop(object)

    def show_all_tasks(self):
        for object in self.vector_of_all_tasks_objects:
            print(f"Task: {object.name}, Date: {object.date}")
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
         with open('addiction.txt', 'r') as f:
             self.x = f.read()  
        
        
        
    def add_addiction(self):
        print("did you gave up to addiction")
        yes_or_no = input()
        print("how much time did you overdoit")
        duration_of_vialonce = input()
        addiction = [yes_or_no, duration_of_vialonce]
        point = [addiction]
        self.allTasks.add_milestone(point)
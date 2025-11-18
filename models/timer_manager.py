# -*- coding: utf-8 -*-
import sqlite3
import sys
import io
import os
from datetime import datetime 
import pandas as pd
from pathlib import Path

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')

class TimerManager:
    def __init__(self):
        self.name_of_timer = 'number_timer.txt'
        if os.path.exists(self.name_of_timer):
            self.path = Path(self.name_of_timer).read_text()
        else:
            self.path = Path(self.name_of_timer)
        
    #we want to create the 
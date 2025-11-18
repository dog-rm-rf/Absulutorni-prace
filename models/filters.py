# -*- coding: utf-8 -*-
import sqlite3
import sys
import io
import os
from datetime import datetime, timedelta
import pandas as pd

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')

class Filter:
    def __init__(self, allTask):
        self.allTask = allTask
    @staticmethod
    def show_task_goals_for_12weeks(self, input_start_date_of_year):
        year = input_start_date_of_year + timedelta(weeks=12)
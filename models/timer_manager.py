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

class 
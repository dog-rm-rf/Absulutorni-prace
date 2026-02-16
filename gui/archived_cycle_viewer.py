"""
Archived Cycle Viewer - zobrazení archivovaného cyklu (read-only)
"""

import pickle
import os
from datetime import datetime, timedelta, date as date_type
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QWidget)
from PyQt5.QtCore import Qt
import pandas as pd


class ArchivedCycleViewer(QDialog):
    """
    Zobrazí archivovaný cyklus v read-only režimu
    """
    
    def __init__(self, cycle_id, archive_file, cycles_manager, parent=None):
        super().__init__(parent)
        self.cycle_id = cycle_id
        self.archive_file = archive_file
        self.cycles_manager = cycles_manager
        self.current_week = 1
        
        # Načti data z archive
        self.load_archive_data()
        
        self.setWindowTitle(f"Cycle #{cycle_id} - Archive")
        self.setModal(True)
        self.resize(1400, 800)
        
        self.setup_ui()
    
    def load_archive_data(self):
        """
        Načte data z archive souboru
        """
        archive_path = os.path.join(self.cycles_manager.archive_dir, self.archive_file)
        
        with open(archive_path, 'rb') as f:
            archive_data = pickle.load(f)
        
        self.metadata = archive_data['metadata']
        self.tasks_df = archive_data.get('tasks')
        self.goals_df = archive_data.get('goals')
        self.notes_df = archive_data.get('notes')
        self.rewards_df = archive_data.get('rewards')
        
        # Převeď DataFrames na listy
        self.tasks = self.tasks_df.values.tolist() if self.tasks_df is not None else []
        self.goals = self.goals_df.values.tolist() if self.goals_df is not None else []
        self.notes = self.notes_df.values.tolist() if self.notes_df is not None else []
        self.rewards = self.rewards_df.values.tolist() if self.rewards_df is not None else []
    
    def setup_ui(self):
        """
        Vytvoří UI
        """
        main_layout = QVBoxLayout()
        
        # ===== HEADER =====
        header_layout = QVBoxLayout()
        
        # Cycle info
        start_date = self.metadata['start_date'].strftime("%d.%m.%Y")
        end_date = self.metadata['end_date'].strftime("%d.%m.%Y")
        
        title = QLabel(f"📦 Cycle #{self.cycle_id} (Archive)")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        title.setAlignment(Qt.AlignCenter)
        
        info = QLabel(f"{start_date} - {end_date}")
        info.setStyleSheet("font-size: 14px; color: lightgray;")
        info.setAlignment(Qt.AlignCenter)
        
        read_only_label = QLabel("🔒 READ ONLY - No editing allowed")
        read_only_label.setStyleSheet("font-size: 12px; color: orange;")
        read_only_label.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(title)
        header_layout.addWidget(info)
        header_layout.addWidget(read_only_label)
        
        main_layout.addLayout(header_layout)
        
        # ===== WEEK NAVIGATION =====
        nav_layout = QHBoxLayout()
        
        self.previous_button = QPushButton("Previous")
        self.previous_button.setStyleSheet("background-color: white; color: black; font-size: 16px;")
        self.previous_button.clicked.connect(self.previous_week)
        self.previous_button.setEnabled(False)  # Week 1 start
        
        self.week_label = QLabel(f"Week {self.current_week}")
        self.week_label.setAlignment(Qt.AlignCenter)
        self.week_label.setStyleSheet("color: white; font-size: 24px;")
        
        self.next_button = QPushButton("Next")
        self.next_button.setStyleSheet("background-color: white; color: black; font-size: 16px;")
        self.next_button.clicked.connect(self.next_week)
        
        nav_layout.addWidget(self.previous_button)
        nav_layout.addWidget(self.week_label)
        nav_layout.addWidget(self.next_button)
        
        main_layout.addLayout(nav_layout)
        
        # ===== DAYS DISPLAY =====
        self.days_scroll = QScrollArea()
        self.days_scroll.setWidgetResizable(True)
        self.days_scroll.setStyleSheet("QScrollArea { border: none; background-color: black; }")
        
        self.update_week_display()
        
        main_layout.addWidget(self.days_scroll)
        
        # ===== CLOSE BUTTON =====
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                padding: 10px;
                font-size: 14px;
            }
        """)
        close_btn.clicked.connect(self.accept)
        
        main_layout.addWidget(close_btn)
        
        self.setLayout(main_layout)
        
        # Styling
        self.setStyleSheet("""
            QDialog {
                background-color: black;
            }
        """)
    
    def update_week_display(self):
        """
        Aktualizuje zobrazení týdne
        """
        # Vypočítej datumy pro aktuální týden
        start_date = self.metadata['start_date']
        week_offset = (self.current_week - 1) * 7
        week_start = start_date + timedelta(days=week_offset)
        
        # Vytvoř widget s dny
        days_widget = QWidget()
        days_layout = QHBoxLayout()
        
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        
        for i in range(7):
            date = week_start + timedelta(days=i)
            day_name = days[i]
            
            # Vytvoř day widget
            day_widget = self.create_day_widget(date, day_name)
            days_layout.addWidget(day_widget)
            
            # Separator
            if i < 6:
                separator = QFrame()
                separator.setFrameShape(QFrame.VLine)
                separator.setStyleSheet("color: white;")
                days_layout.addWidget(separator)
        
        days_widget.setLayout(days_layout)
        self.days_scroll.setWidget(days_widget)
    
    def create_day_widget(self, date, day_name):
        """
        Vytvoří widget pro jeden den
        """
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: black;
                border: 1px solid white;
            }
        """)
        widget.setMaximumWidth(200)
        
        layout = QVBoxLayout()
        
        # Datum
        date_label = QLabel(f"{day_name}\n{date.day}.{date.month}")
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(date_label)
        
        # Tasks pro tento den
        tasks_for_day = [t for t in self.tasks if self.same_date(t[2], date)]
        
        for task in tasks_for_day:
            task_name = task[0]
            task_hours = task[3]
            task_score = task[4] if len(task) > 4 else None
            
            # Ikona
            icon = "✅" if task_score is not None else "•"
            
            # Zkrať název
            display_name = task_name[:18] + "..." if len(task_name) > 18 else task_name
            
            task_label = QLabel(f"{icon} {display_name}\n   ({task_hours}h)")
            task_label.setStyleSheet("color: lightgray; font-size: 14px; padding-left: 10px;")
            task_label.setToolTip(task_name)
            layout.addWidget(task_label)
        
        # Notes
        notes_for_day = [n for n in self.notes if self.same_date(n[0], date)]
        
        for note in notes_for_day:
            note_topic = note[2]
            display_topic = note_topic[:18] + "..." if len(note_topic) > 18 else note_topic
            
            note_label = QLabel(f"📝 {display_topic}")
            note_label.setStyleSheet("color: #FFA500; font-size: 14px; padding-left: 10px;")
            note_label.setToolTip(note_topic)
            layout.addWidget(note_label)
        
        # Rewards
        rewards_for_day = [r for r in self.rewards if self.same_date(r[0], date)]
        
        for reward in rewards_for_day:
            reward_name = reward[1]
            reward_finished = reward[3]
            
            icon = "✅" if reward_finished else "🎁"
            display_reward = reward_name[:18] + "..." if len(reward_name) > 18 else reward_name
            
            reward_label = QLabel(f"{icon} {display_reward}")
            reward_label.setStyleSheet("color: #00FF00; font-size: 14px; padding-left: 10px;")
            reward_label.setToolTip(reward_name)
            layout.addWidget(reward_label)
        
        layout.addStretch()
        widget.setLayout(layout)
        
        return widget
    
    def to_date(self, value):
        """
        Bezpečně převede jakýkoliv datumový typ na datetime.date
        
        Zvládne: datetime, date, pandas.Timestamp
        
        Args:
            value: Datumová hodnota libovolného typu
            
        Returns:
            datetime.date
        """
        if isinstance(value, datetime):
            return value.date()
        elif isinstance(value, date_type):
            return value
        elif isinstance(value, pd.Timestamp):
            return value.date()
        else:
            # Fallback — zkus převést přes str
            return value
    
    def same_date(self, date1, date2):
        """
        Porovná dvě data (ignoruje čas)
        Zvládne datetime, date i pandas.Timestamp
        """
        return self.to_date(date1) == self.to_date(date2)
    
    def previous_week(self):
        """
        Přejde na předchozí týden
        """
        self.current_week -= 1
        self.week_label.setText(f"Week {self.current_week}")
        
        self.next_button.setEnabled(True)
        
        if self.current_week <= 1:
            self.previous_button.setEnabled(False)
        
        self.update_week_display()
    
    def next_week(self):
        """
        Přejde na další týden
        """
        self.current_week += 1
        self.week_label.setText(f"Week {self.current_week}")
        
        self.previous_button.setEnabled(True)
        
        if self.current_week >= 12:
            self.next_button.setEnabled(False)
        
        self.update_week_display()      
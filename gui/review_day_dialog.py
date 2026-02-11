"""
Review Day Dialog - přidání score a review k taskům
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QWidget, QTextEdit,
                             QSpinBox, QFrame)
from PyQt5.QtCore import Qt
from datetime import datetime


class ReviewDayDialog(QDialog):
    """
    Dialog pro review tasků daného dne
    """
    
    def __init__(self, date, tasks, parent=None):
        super().__init__(parent)
        self.date = date
        self.tasks = tasks
        self.review_data = []  # [(task_index, score, went_well, didnt_work, improve), ...]
        
        self.setWindowTitle(f"Review Day - {date.strftime('%d.%m.%Y')}")
        self.setModal(True)
        self.setMinimumSize(700, 500)
        
        self.setup_ui()
    
    def setup_ui(self):
        """
        Vytvoří UI
        """
        main_layout = QVBoxLayout()
        
        # Nadpis
        title = QLabel(f"Review Day - {self.date.strftime('%d.%m.%Y')}")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        if not self.tasks:
            # Žádné tasky
            no_tasks_label = QLabel("No tasks for this day")
            no_tasks_label.setAlignment(Qt.AlignCenter)
            no_tasks_label.setStyleSheet("color: grey; font-size: 14px; padding: 50px;")
            main_layout.addWidget(no_tasks_label)
        else:
            # Scroll area pro tasky
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("QScrollArea { border: none; }")
            
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout()
            
            # Pro každý task vytvoř review panel
            self.task_panels = []
            for i, task in enumerate(self.tasks):
                task_panel = self.create_task_panel(task, i)
                scroll_layout.addWidget(task_panel)
                self.task_panels.append(task_panel)
            
            scroll_widget.setLayout(scroll_layout)
            scroll.setWidget(scroll_widget)
            main_layout.addWidget(scroll)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #3D3D3D;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        save_btn.clicked.connect(self.save_reviews)
        
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(save_btn)
        
        main_layout.addLayout(buttons_layout)
        
        self.setLayout(main_layout)
        
        # Styling dialogu - černý jako zbytek aplikace
        self.setStyleSheet("""
            QDialog {
                background-color: black;
            }
        """)
    
    def create_task_panel(self, task, task_index):
        """
        Vytvoří panel pro review jednoho tasku
        """
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: black;
                border: 1px solid white;
                padding: 15px;
                margin: 5px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Task info
        task_name = task[0]
        task_subclass = task[1] if len(task) > 1 else ""
        task_hours = task[3] if len(task) > 3 else 0
        
        # Načti existující review data
        current_score = task[4] if len(task) > 4 and task[4] is not None else 0
        current_review = task[5] if len(task) > 5 else []
        
        # Rozbal review na 3 části
        went_well = ""
        didnt_work = ""
        improve = ""
        
        if isinstance(current_review, list) and len(current_review) >= 3:
            went_well = current_review[0] if current_review[0] else ""
            didnt_work = current_review[1] if current_review[1] else ""
            improve = current_review[2] if current_review[2] else ""
        
        # Název tasku
        name_label = QLabel(f"{task_name}")
        name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        layout.addWidget(name_label)
        
        # Subclass a hours
        info_label = QLabel(f"{task_subclass} | {task_hours}h")
        info_label.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(info_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: white;")
        layout.addWidget(separator)
        
        # Score input
        score_layout = QHBoxLayout()
        score_label = QLabel("Score (0-10):")
        score_label.setStyleSheet("color: white; font-size: 14px;")
        
        score_input = QSpinBox()
        score_input.setMinimum(0)
        score_input.setMaximum(10)
        score_input.setValue(int(current_score) if current_score else 0)
        score_input.setStyleSheet("""
            QSpinBox {
                background-color: black;
                color: white;
                border: 1px solid white;
                padding: 5px;
                font-size: 14px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: black;
                border: 1px solid white;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: white;
            }
            QSpinBox::up-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 5px solid white;
                width: 0px;
                height: 0px;
            }
            QSpinBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid white;
                width: 0px;
                height: 0px;
            }
        """)
        
        score_layout.addWidget(score_label)
        score_layout.addWidget(score_input)
        score_layout.addStretch()
        layout.addLayout(score_layout)
        
        # Review - 3 části
        
        # 1. Co se povedlo
        went_well_label = QLabel("What went well:")
        went_well_label.setStyleSheet("color: white; font-size: 14px; margin-top: 10px;")
        layout.addWidget(went_well_label)
        
        went_well_input = QTextEdit()
        went_well_input.setPlaceholderText("What worked well? What are you proud of?")
        went_well_input.setMaximumHeight(60)
        went_well_input.setPlainText(went_well)
        went_well_input.setStyleSheet("""
            QTextEdit {
                background-color: black;
                color: white;
                border: 1px solid white;
                padding: 5px;
                font-size: 14px;
            }
        """)
        layout.addWidget(went_well_input)
        
        # 2. Co se nepovedlo
        didnt_work_label = QLabel("What didn't work:")
        didnt_work_label.setStyleSheet("color: white; font-size: 14px; margin-top: 5px;")
        layout.addWidget(didnt_work_label)
        
        didnt_work_input = QTextEdit()
        didnt_work_input.setPlaceholderText("What challenges did you face?")
        didnt_work_input.setMaximumHeight(60)
        didnt_work_input.setPlainText(didnt_work)
        didnt_work_input.setStyleSheet("""
            QTextEdit {
                background-color: black;
                color: white;
                border: 1px solid white;
                padding: 5px;
                font-size: 14px;
            }
        """)
        layout.addWidget(didnt_work_input)
        
        # 3. Co zlepšit
        improve_label = QLabel("What to improve:")
        improve_label.setStyleSheet("color: white; font-size: 14px; margin-top: 5px;")
        layout.addWidget(improve_label)
        
        improve_input = QTextEdit()
        improve_input.setPlaceholderText("What will you do differently next time?")
        improve_input.setMaximumHeight(60)
        improve_input.setPlainText(improve)
        improve_input.setStyleSheet("""
            QTextEdit {
                background-color: black;
                color: white;
                border: 1px solid white;
                padding: 5px;
                font-size: 14px;
            }
        """)
        layout.addWidget(improve_input)
        
        panel.setLayout(layout)
        
        # Ulož reference
        panel.task_index = task_index
        panel.score_input = score_input
        panel.went_well_input = went_well_input
        panel.didnt_work_input = didnt_work_input
        panel.improve_input = improve_input
        
        return panel
    
    def save_reviews(self):
        """
        Uloží všechny reviews
        """
        self.review_data = []
        
        for panel in self.task_panels:
            task_index = panel.task_index
            score = panel.score_input.value()
            went_well = panel.went_well_input.toPlainText().strip()
            didnt_work = panel.didnt_work_input.toPlainText().strip()
            improve = panel.improve_input.toPlainText().strip()
            
            self.review_data.append((task_index, score, went_well, didnt_work, improve))
        
        print(f"✅ Uloženo {len(self.review_data)} reviews")
        
        self.accept()
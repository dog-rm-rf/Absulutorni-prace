"""
Edit Goal Dialog - editace existujícího goalu
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLabel, 
                             QLineEdit, QSpinBox, QPushButton, QHBoxLayout,
                             QMessageBox)
from PyQt5.QtCore import Qt


class EditGoalDialog(QDialog):
    """
    Dialog pro editaci goalu
    NELZE měnit subclass (kategorie) - aby se neztratily statistiky!
    """
    
    def __init__(self, goal, parent=None):
        super().__init__(parent)
        
        # Ulož původní goal
        self.original_goal = goal
        self.goal_data = None
        
        # goal = [name, subclass, timer, score, start, checked, end, completed]
        self.goal_name = goal[0]
        self.goal_subclass = goal[1]  # NELZE MĚNIT!
        self.goal_timer = goal[2]
        self.goal_score = goal[3]
        self.goal_start = goal[4]
        self.goal_checked = goal[5] if len(goal) > 5 else False
        self.goal_end = goal[6] if len(goal) > 6 else None
        self.goal_completed = goal[7] if len(goal) > 7 else False
        
        self.setWindowTitle("Edit Goal")
        self.setModal(True)
        self.setMinimumSize(400, 300)
        
        self.setup_ui()
    
    def setup_ui(self):
        """
        Vytvoří UI
        """
        main_layout = QVBoxLayout()
        
        # Header
        title = QLabel(f"Edit Goal: {self.goal_name}")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        
        # Subclass (READ-ONLY - zobrazit ale nelze měnit)
        subclass_label = QLabel(self.goal_subclass)
        subclass_label.setStyleSheet("color: lightgray; font-style: italic;")
        
        warning = QLabel("(Category cannot be changed to preserve statistics)")
        warning.setStyleSheet("color: orange; font-size: 10px;")
        
        form_layout.addRow("Category:", subclass_label)
        form_layout.addRow("", warning)
        
        # Goal Name
        self.name_input = QLineEdit()
        self.name_input.setText(self.goal_name)
        self.name_input.setPlaceholderText("e.g. Be better programmer")
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: black;
                color: white;
                border: 1px solid white;
                padding: 5px;
            }
        """)
        form_layout.addRow("Goal Name:", self.name_input)
        
        # Target Hours
        self.hours_input = QSpinBox()
        self.hours_input.setMinimum(1)
        self.hours_input.setMaximum(1000)
        self.hours_input.setValue(int(self.goal_timer))
        self.hours_input.setSuffix(" h")
        self.hours_input.setStyleSheet("""
            QSpinBox {
                background-color: black;
                color: white;
                border: 1px solid white;
                padding: 5px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: black;
                border: 1px solid white;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: white;
            }
            QSpinBox::up-arrow {
                border-bottom: 5px solid white;
            }
            QSpinBox::down-arrow {
                border-top: 5px solid white;
            }
        """)
        form_layout.addRow("Target Hours:", self.hours_input)
        
        # Target Avg Score
        self.score_input = QSpinBox()
        self.score_input.setMinimum(0)
        self.score_input.setMaximum(10)
        self.score_input.setValue(int(self.goal_score))
        self.score_input.setSuffix(" / 10")
        self.score_input.setStyleSheet("""
            QSpinBox {
                background-color: black;
                color: white;
                border: 1px solid white;
                padding: 5px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: black;
                border: 1px solid white;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: white;
            }
            QSpinBox::up-arrow {
                border-bottom: 5px solid white;
            }
            QSpinBox::down-arrow {
                border-top: 5px solid white;
            }
        """)
        form_layout.addRow("Target Avg Score:", self.score_input)
        
        main_layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #3D3D3D;
                color: white;
                padding: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Save Changes")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                padding: 10px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        save_btn.clicked.connect(self.save_changes)
        
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(save_btn)
        
        main_layout.addLayout(buttons_layout)
        
        self.setLayout(main_layout)
        
        # Styling
        self.setStyleSheet("""
            QDialog {
                background-color: black;
            }
            QLabel {
                color: white;
            }
        """)
    
    def save_changes(self):
        """
        Uloží změny
        """
        # Získej hodnoty
        new_name = self.name_input.text().strip()
        new_hours = self.hours_input.value()
        new_score = self.score_input.value()
        
        # Validace
        if not new_name:
            QMessageBox.warning(self, "Error", "Goal name cannot be empty!")
            return
        
        # Vytvoř aktualizovaný goal
        # DŮLEŽITÉ: Subclass (kategorie) zůstává STEJNÁ!
        self.goal_data = [
            new_name,                # 0 - nový název
            self.goal_subclass,      # 1 - PŮVODNÍ kategorie (NELZE MĚNIT)
            new_hours,               # 2 - nové hodiny
            new_score,               # 3 - nový target score
            self.goal_start,         # 4 - původní start date
            self.goal_checked,       # 5 - původní checked
            self.goal_end,           # 6 - původní end date
            self.goal_completed      # 7 - původní completed
        ]
        
        print(f"✅ Goal edited: {new_name} (category: {self.goal_subclass} unchanged)")
        
        self.accept()


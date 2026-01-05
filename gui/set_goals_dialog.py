from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QScrollArea, 
                             QWidget)
from PyQt5.QtCore import Qt


class SetGoalsDialog(QDialog):
    """
    Popup dialog pro nastavení goals
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.goals_data = []  # List goals které uživatel zadá
        self.goal_rows = []  # List všech goal řádků (widgets)  
        
        # Nastavení okna
        self.setWindowTitle("Set Your Goals")
        self.setModal(True)
        self.setFixedSize(600, 500)
        
        # Layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10) 
        
        # Nadpis
        title_label = QLabel("Set Goals for the Next 12 Weeks")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True) 
        title_label.setFixedHeight(50)
        title_label.setStyleSheet("""
            font-size: 18px;    
            font-weight: bold;
            padding: 10px;
        """)
        main_layout.addWidget(title_label)
        
        # Popis
        description_label = QLabel(
            "These goals will guide your tasks and activities.\n"
            "Be specific and measurable!"
        )
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setWordWrap(True)
        description_label.setFixedHeight(50) 
        description_label.setStyleSheet("""
            color: gray;
            font-size: 13px;
            padding: 5px;
        """)
        main_layout.addWidget(description_label)
        
        # Spacing
        main_layout.addSpacing(10)
        
        # ===== SCROLLABLE AREA PRO GOALS =====
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        # Widget uvnitř scroll area
        scroll_widget = QWidget()
        self.goals_layout = QVBoxLayout()  # Layout pro goal řádky
        self.goals_layout.setSpacing(10)
        scroll_widget.setLayout(self.goals_layout)
        
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        
        # ===== ADD GOAL BUTTON =====
        add_goal_button = QPushButton("+ Add Goal")
        add_goal_button.setFixedHeight(40)
        add_goal_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        add_goal_button.clicked.connect(self.add_goal_row)
        main_layout.addWidget(add_goal_button)
        
        # ===== SAVE BUTTON =====
        save_button = QPushButton("Save Goals")
        save_button.setFixedHeight(50)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_button.clicked.connect(self.save_goals)
        main_layout.addWidget(save_button)
        
        self.setLayout(main_layout)
        
        # Vytvoř 1 výchozí goal
        self.add_goal_row()
        
        
    def add_goal_row(self):
        """
        Přidá nový řádek s goal inputem
        """
        # Container pro tento goal (horizontal layout)
        row_widget = QWidget()
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(5)
        
        # Číslo goalu
        goal_number = len(self.goal_rows) + 1
        number_label = QLabel(f"Goal {goal_number}:")
        number_label.setFixedWidth(70)
        number_label.setStyleSheet("font-size: 14px;")
        row_layout.addWidget(number_label)
        
        # Input pro goal název
        goal_input = QLineEdit()
        goal_input.setPlaceholderText(f"Goal name...")
        goal_input.setFixedHeight(40)
        goal_input.setStyleSheet("""
            padding: 8px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 3px;
        """)
        row_layout.addWidget(goal_input, stretch=3)  # 3x větší než ostatní
        
        # Input pro subclass
        subclass_input = QLineEdit()
        subclass_input.setPlaceholderText("Category")
        subclass_input.setFixedHeight(40)
        subclass_input.setStyleSheet("""
            padding: 8px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 3px;
        """)
        row_layout.addWidget(subclass_input, stretch=2)
        
        # Input pro timer (hodiny)
        timer_input = QLineEdit()
        timer_input.setPlaceholderText("Hours")
        timer_input.setFixedHeight(40)
        timer_input.setStyleSheet("""
            padding: 8px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 3px;
        """)
        row_layout.addWidget(timer_input, stretch=1)
        
        # Input pro průměrné score
        score_input = QLineEdit()
        score_input.setPlaceholderText("Score")
        score_input.setFixedHeight(40)
        score_input.setStyleSheet("""
            padding: 8px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 3px;
        """)
        row_layout.addWidget(score_input, stretch=1)
        
        # Remove button (X)
        remove_button = QPushButton("✕")
        remove_button.setFixedSize(40, 40)
        remove_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        remove_button.clicked.connect(lambda: self.remove_goal_row(row_widget))
        row_layout.addWidget(remove_button)
        
        row_widget.setLayout(row_layout)
        
        # Přidej do layoutu
        self.goals_layout.addWidget(row_widget)
                             
        # Ulož referenci (widget + input)
        self.goal_rows.append({
            'widget': row_widget,
            'input': goal_input,
            'subclass_input': subclass_input,      
            'timer_input': timer_input,            
            'score_input': score_input,
            'number_label': number_label
        })
        
        # Update číslování
        self.update_goal_numbers()
        
    def remove_goal_row(self, row_widget):
        """
        Odstraní goal řádek
        """
        # Nesmí být méně než 1 goal
        if len(self.goal_rows) <= 1:
            QMessageBox.warning(
                self,
                "Minimum 1 Goal",
                "You must have at least 1 goal!\n\n"
                "Keep pushing yourself! 💪"
            )
            return
        
        # Najdi a odstraň z goal_rows
        for i, row_data in enumerate(self.goal_rows):
            if row_data['widget'] == row_widget:
                # Odstraň widget z GUI
                self.goals_layout.removeWidget(row_widget)
                row_widget.deleteLater()
                
                # Odstraň z listu
                self.goal_rows.pop(i)
                break
        
        # Update číslování
        self.update_goal_numbers() 
        
    def update_goal_numbers(self):
        """
        Aktualizuje čísla goals (Goal 1, Goal 2, ...)
        """
        for i, row_data in enumerate(self.goal_rows):
            row_data['number_label'].setText(f"Goal {i+1}:")
            row_data['input'].setPlaceholderText(f"Enter goal {i+1}...")
    
    def save_goals(self):
        """
        Validuje a uloží goals
        """
        # Získej všechny goals
        goals = []
        
        for row_data in self.goal_rows:
            goal_name = row_data['input'].text().strip()
            subclass = row_data['subclass_input'].text().strip()
            timer_str = row_data['timer_input'].text().strip()
            score_str = row_data['score_input'].text().strip()
            
            # Validace - goal_name musí být vyplněný
            if not goal_name:
                continue
            
            # Převeď timer na číslo (default 0)
            try:
                timer = float(timer_str) if timer_str else 0.0
            except ValueError:
                timer = 0.0
                
            # Převeď score na číslo (default 0)
            try:
                score = float(score_str) if score_str else 0.0
            except ValueError:
                score = 0.0
                
            # Ulož jako list
            goals.append([
                goal_name,
                subclass if subclass else "general",
                timer,
                score
            ])
        
        # Validace - minimálně 1 goal
        if len(goals) < 1:
            QMessageBox.warning(
                self,
                "Not Enough Goals",
                "Please enter at least 1 goal.\n\n"
                "Empty goals won't be saved!"
            )
            return
        
        # Uložit goals
        self.goals_data = goals
        
        # Zavřít dialog
        self.accept()    
        
    #     # 5 input polí pro goals
    #     self.goal_inputs = []
        
    #     for i in range(5):
    #         # Label
    #         label_text = f"Goal {i+1}:"
    #         if i >= 3:
    #             label_text += " (optional)"
            
    #         goal_label = QLabel(label_text)
    #         goal_label.setFixedHeight(25)
    #         goal_label.setStyleSheet("font-size: 14px;")
    #         layout.addWidget(goal_label)
            
    #         # Input
    #         goal_input = QLineEdit()
    #         goal_input.setPlaceholderText(f"Enter goal {i+1}...")
    #         goal_input.setFixedHeight(40) 
    #         goal_input.setStyleSheet("""
    #             padding: 8px;
    #             font-size: 14px;
    #             border: 1px solid #ccc;
    #             border-radius: 3px;
    #         """)    
    #         layout.addWidget(goal_input)
            
    #         # Uložit input do listu
    #         self.goal_inputs.append(goal_input)
        
    #     # Spacing
    #     layout.addSpacing(20)
        
    #     # Save button
    #     save_button = QPushButton("Save Goals")
    #     save_button.setFixedHeight(50)
    #     save_button.setStyleSheet("""
    #         QPushButton {
    #             background-color: white;
    #             color: black;
    #             font-size: 16px;
    #             font-weight: bold;
    #             padding: 12px;
    #             border-radius: 5px;
    #             border: none;
    #         }
    #         QPushButton:hover {
    #             background-color: white;
    #         }
    #     """)
    #     save_button.clicked.connect(self.save_goals)
    #     layout.addWidget(save_button)
        
    #     # Přidej stretch na konec (tlačí všechno nahoru)
    #     layout.addStretch()
        
    #     self.setLayout(layout)
    
    # def save_goals(self):
    #     """
    #     Validuje a uloží goals
    #     """
    #     # Získej všechny goals z inputů
    #     goals = []
        
    #     for _, goal_input in enumerate(self.goal_inputs):
    #         goal_text = goal_input.text().strip()
    #         if goal_text:
    #             goals.append(goal_text)
        
    #     # Validace - minimálně 3 goals
    #     if len(goals) < 3:
    #         QMessageBox.warning(
    #             self,
    #             "Not Enough Goals",
    #             "Please enter at least 3 goals.\n\n"
    #             "Goals help you stay focused during the 12 weeks!"
    #         )
    #         return
        
    #     # Uložit goals
    #     self.goals_data = goals
        
    #     # Zavřít dialog s úspěchem
    #     self.accept()
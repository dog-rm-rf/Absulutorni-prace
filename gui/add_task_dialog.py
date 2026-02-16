from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLabel, 
                            QLineEdit, QSpinBox, QHBoxLayout, QPushButton, QComboBox, QMessageBox)


# ===== DIALOG PRO PŘIDÁNÍ TASKU =====
class AddTaskDialog(QDialog):
    """
    Popup dialog pro přidání nového tasku
    """
    def __init__(self, date, parent=None, goals=None):
        super().__init__(parent)
        self.date = date
        self.task_data = None  # Sem uložíme data když user klikne Save
        self.goals = goals or []
        
        # Nastavení okna
        self.setWindowTitle("Add Task")
        self.setModal(True)  # Blokuje hlavní okno dokud se nezavře
        self.setFixedSize(400, 250)
        
        # Layout
        layout = QVBoxLayout()
        
        # Formulář
        form_layout = QFormLayout()
        
        # Datum (read-only, jen zobrazení)
        date_label = QLabel(date.strftime("%d.%m.%Y"))
        date_label.setStyleSheet("color: gray;")
        form_layout.addRow("Date:", date_label)
        
        # Task Name
        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("Enter task name")
        form_layout.addRow("Task Name:", self.task_name_input)
        
        # Subclass
        self.subclass_input = QComboBox()
        self.subclass_input.setEditable(True)
        self.subclass_input.setPlaceholderText("Select or type category...")

        # Načti kategorie z goals
        categories = self.get_categories_from_goals()

        if categories:
            self.subclass_input.addItems(categories)
        else:
            # Žádné goals - defaultní kategorie
            self.subclass_input.addItems(["general", "programming", "learning", "fitness"])
        
        self.subclass_input.setStyleSheet("""
            QComboBox {
                background-color: black;
                color: white;
                border: 1px solid white;
                padding: 3px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: black;
                color: white;
                selection-background-color: #3D3D3D;
                border: 1px solid white;
            }
        """)

        form_layout.addRow("Subclass:", self.subclass_input)
        
        # Hours a Minutes - vytvoř horizontal layout
        time_layout = QHBoxLayout()
        
        # Hours SpinBox
        self.hours_input = QSpinBox()
        self.hours_input.setMinimum(0)
        self.hours_input.setMaximum(24)
        self.hours_input.setValue(2)  # Default 2 hodiny
        self.hours_input.setSuffix(" h")  # Přidá "h" za číslo
        
        # Minutes SpinBox
        self.minutes_input = QSpinBox()
        self.minutes_input.setMinimum(0)
        self.minutes_input.setMaximum(59)
        self.minutes_input.setSingleStep(15)  # Krok po 15 minutách
        self.minutes_input.setValue(0)  # Default 0 minut
        self.minutes_input.setSuffix(" min")  # Přidá "min" za číslo
        
        # Přidej oba do horizontal layoutu
        time_layout.addWidget(self.hours_input)
        time_layout.addWidget(self.minutes_input)
        
        # Přidej celý time_layout do formuláře
        form_layout.addRow("Time:", time_layout)
        
        layout.addLayout(form_layout)
        
        # Buttons (Cancel, Save)
        buttons_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)  # Zavře dialog bez uložení
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_task)
        save_button.setStyleSheet("background-color: #FFFFFF; color: black;")
        
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(save_button)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        

    def get_categories_from_goals(self):
        """
        Načte unikátní kategorie (subclass) z goals
        
        Returns:
            list: ["programming", "learning", "fitness", ...]
        """
        categories = []
        
        for goal in self.goals:
            if len(goal) > 1:
                subclass = goal[1]  # Index 1 = subclass
                if subclass and subclass not in categories:
                    categories.append(subclass)
        
        return sorted(categories)  # Abecedně seřazené
    
    def save_task(self):
        """
        Uloží data a zavře dialog
        """
        # Získej hodnoty z inputů
        task_name = self.task_name_input.text().strip()
        subclass = self.subclass_input.currentText().strip()
        # Získej hodiny a minuty
        hours = self.hours_input.value()
        minutes = self.minutes_input.value()
        
        # Převeď na desetinné číslo (např. 2h 30min = 2.5)
        total_hours = hours + (minutes / 60.0)
        
        # Validace
        if not task_name:
            QMessageBox.warning(self, "Missing Task Name", "Please enter a task name.")
            return
        
        # Ulož data (v formátu pro all_tasks.add_new_task)
        # [task_name, task_sub_class, task_date, desired_time_spent, score, review]
        self.task_data = [
            task_name,
            subclass if subclass else "general",  # Default subclass
            self.date,
            total_hours,
            None,  # score (zatím None)
            ["", "", ""]  # review (learnt, dont_understand, next_step)
        ]
        
        # Zavři dialog s úspěchem
        self.accept()
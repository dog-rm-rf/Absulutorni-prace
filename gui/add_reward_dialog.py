from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLabel, 
                             QLineEdit, QSpinBox, QHBoxLayout, QPushButton)


# ===== DIALOG PRO PŘIDÁNÍ REWARD =====
class AddRewardDialog(QDialog):
    """
    Popup dialog pro přidání odměny
    """
    def __init__(self, date, parent=None):
        super().__init__(parent)
        self.date = date
        self.reward_data = None
        
        # Nastavení okna
        self.setWindowTitle("Add Reward")
        self.setModal(True)
        self.setFixedSize(400, 250)
        
        # Layout
        layout = QVBoxLayout()
        
        # Formulář
        form_layout = QFormLayout()
        
        # Datum (read-only)
        date_label = QLabel(date.strftime("%d.%m.%Y"))
        date_label.setStyleSheet("color: gray;")
        form_layout.addRow("Date:", date_label)
        
        # Reward Name
        self.reward_name_input = QLineEdit()
        self.reward_name_input.setPlaceholderText("e.g. Watch movie, Play games")
        form_layout.addRow("Reward:", self.reward_name_input)
        
        # Time - Hours and Minutes
        time_layout = QHBoxLayout()
        
        self.hours_input = QSpinBox()
        self.hours_input.setMinimum(0)
        self.hours_input.setMaximum(24)
        self.hours_input.setValue(1)
        self.hours_input.setSuffix(" h")
        
        self.minutes_input = QSpinBox()
        self.minutes_input.setMinimum(0)
        self.minutes_input.setMaximum(59)
        self.minutes_input.setSingleStep(15)
        self.minutes_input.setValue(0)
        self.minutes_input.setSuffix(" min")
        
        time_layout.addWidget(self.hours_input)
        time_layout.addWidget(self.minutes_input)
        
        form_layout.addRow("Time:", time_layout)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_reward)
        save_button.setStyleSheet("background-color: white; color: black;")
        
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(save_button)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def save_reward(self):
        """
        Uloží reward data
        """
        # Získej hodnoty
        reward_name = self.reward_name_input.text().strip()
        hours = self.hours_input.value()
        minutes = self.minutes_input.value()
        
        # Validace
        if not reward_name:
            print("ERROR: Reward name is required!")
            return
        
        # Převeď na desetinné číslo
        total_hours = hours + (minutes / 60.0)
        
        # Ulož data (v formátu pro reward.add_reward)
        # [date_of_creation, reward_name, time, finished]
        self.reward_data = [
            self.date,
            reward_name,
            total_hours,
            False, # finished = False (ještě nesplněno)
            total_hours,
        ]
        
        # Zavři dialog
        self.accept()
"""
Review Rewards Dialog - review splnění rewards
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QWidget, QFrame,
                             QRadioButton, QButtonGroup, QDoubleSpinBox)
from PyQt5.QtCore import Qt


class ReviewRewardsDialog(QDialog):
    """
    Dialog pro review rewards daného dne
    """
    
    def __init__(self, date, rewards, parent=None):
        super().__init__(parent)
        self.date = date
        self.rewards = rewards
        self.review_data = []  # [(reward_index, completed, actual_time), ...]
        
        self.setWindowTitle(f"Review Rewards - {date.strftime('%d.%m.%Y')}")
        self.setModal(True)
        self.setMinimumSize(600, 400)
        
        self.setup_ui()
    
    def setup_ui(self):
        """
        Vytvoří UI
        """
        main_layout = QVBoxLayout()
        
        # Nadpis
        title = QLabel(f"Review Rewards - {self.date.strftime('%d.%m.%Y')}")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        if not self.rewards:
            # Žádné rewards
            no_rewards_label = QLabel("No rewards for this day")
            no_rewards_label.setAlignment(Qt.AlignCenter)
            no_rewards_label.setStyleSheet("color: gray; font-size: 14px; padding: 50px;")
            main_layout.addWidget(no_rewards_label)
        else:
            # Scroll area pro rewards
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("QScrollArea { border: none; }")
            
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout()
            
            # Pro každou reward vytvoř panel
            self.reward_panels = []
            for i, reward in enumerate(self.rewards):
                reward_panel = self.create_reward_panel(reward, i)
                scroll_layout.addWidget(reward_panel)
                self.reward_panels.append(reward_panel)
            
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
        
        # Styling dialogu
        self.setStyleSheet("""
            QDialog {
                background-color: black;
            }
        """)
    
    def create_reward_panel(self, reward, reward_index):
        """
        Vytvoří panel pro review jedné reward
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
        
        # Reward info
        reward_name = reward[1]
        reward_time = reward[2]  # Plánovaný čas
        current_finished = reward[3] if len(reward) > 3 else False
        current_actual_time = reward[4] if len(reward) > 4 else reward_time
        
        # Název reward
        name_label = QLabel(f"🎁 {reward_name}")
        name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        layout.addWidget(name_label)
        
        # Plánovaný čas
        info_label = QLabel(f"Planned time: {reward_time}h")
        info_label.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(info_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: white;")
        layout.addWidget(separator)
        
        # Did you complete it?
        completed_label = QLabel("Did you complete this reward?")
        completed_label.setStyleSheet("color: white; font-size: 14px; margin-top: 10px;")
        layout.addWidget(completed_label)
        
        # Radio buttons
        radio_layout = QHBoxLayout()
        
        button_group = QButtonGroup()
        
        yes_radio = QRadioButton("Yes")
        yes_radio.setStyleSheet("color: white; font-size: 14px;")
        yes_radio.setChecked(current_finished)
        
        no_radio = QRadioButton("No")
        no_radio.setStyleSheet("color: white; font-size: 14px;")
        no_radio.setChecked(not current_finished)
        
        button_group.addButton(yes_radio)
        button_group.addButton(no_radio)
        
        radio_layout.addWidget(yes_radio)
        radio_layout.addWidget(no_radio)
        radio_layout.addStretch()
        
        layout.addLayout(radio_layout)
        
        # Actual time spent (pokud No)
        time_label = QLabel("How much time did you actually spend?")
        time_label.setStyleSheet("color: white; font-size: 14px; margin-top: 10px;")
        
        time_input = QDoubleSpinBox()
        time_input.setMinimum(0)
        time_input.setMaximum(24)
        time_input.setSingleStep(0.5)
        time_input.setValue(current_actual_time)
        time_input.setSuffix(" h")
        time_input.setStyleSheet("""
            QDoubleSpinBox {
                background-color: black;
                color: white;
                border: 1px solid white;
                padding: 5px;
                font-size: 14px;
            }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                background-color: black;
                border: 1px solid white;
            }
            QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
                background-color: white;
            }
            QDoubleSpinBox::up-arrow {
                border-bottom: 5px solid white;
            }
            QDoubleSpinBox::down-arrow {
                border-top: 5px solid white;
            }
        """)
        
        # Zobrazuj time input jen když je No
        def toggle_time_input():
            visible = no_radio.isChecked()
            time_label.setVisible(visible)
            time_input.setVisible(visible)
        
        yes_radio.toggled.connect(toggle_time_input)
        toggle_time_input()  # Initial state
        
        layout.addWidget(time_label)
        layout.addWidget(time_input)
        
        panel.setLayout(layout)
        
        # Ulož reference
        panel.reward_index = reward_index
        panel.yes_radio = yes_radio
        panel.no_radio = no_radio
        panel.time_input = time_input
        
        return panel
    
    def save_reviews(self):
        """
        Uloží všechny reviews
        """
        self.review_data = []
        
        for panel in self.reward_panels:
            reward_index = panel.reward_index
            completed = panel.yes_radio.isChecked()
            actual_time = panel.time_input.value()
            
            self.review_data.append((reward_index, completed, actual_time))
        
        print(f"✅ Uloženo {len(self.review_data)} reward reviews")
        
        self.accept()
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                             QListWidget, QListWidgetItem, QPushButton, QLabel,
                             QMessageBox, QWidget)
from PyQt5.QtCore import Qt
from .set_goals_dialog import SetGoalsDialog
from .add_task_dialog import AddTaskDialog
from .add_note_dialog import AddNoteDialog
from .add_reward_dialog import AddRewardDialog
from datetime import datetime


class ManagementDialog(QDialog):
    """
    Dialog pro správu Goals, Tasks, Rewards, Notes
    """
    def __init__(self, parent, all_tasks, goal, note, reward):
        super().__init__(parent)
        self.parent_window = parent
        self.all_tasks = all_tasks
        self.goal = goal
        self.note = note
        self.reward = reward
        
        # Nastavení okna
        self.setWindowTitle("Manage Data")
        self.setModal(True)
        self.setMinimumSize(800, 600)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Vytvoř jednotlivé taby
        self.goals_tab = self.create_goals_tab()
        self.tasks_tab = self.create_tasks_tab()
        self.rewards_tab = self.create_rewards_tab()
        self.notes_tab = self.create_notes_tab()
        
        self.tabs.addTab(self.goals_tab, "Goals")
        self.tabs.addTab(self.tasks_tab, "Tasks")
        self.tabs.addTab(self.rewards_tab, "Rewards")
        self.tabs.addTab(self.notes_tab, "Notes")
        
        main_layout.addWidget(self.tabs)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        main_layout.addWidget(close_button)
        
        self.setLayout(main_layout)
    
    # ===== GOALS TAB =====
    def create_goals_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Info label
        info_label = QLabel("Goals for Current Cycle")
        info_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(info_label)
        
        # List widget
        self.goals_list = QListWidget()
        self.refresh_goals_list()
        layout.addWidget(self.goals_list)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Goal")
        add_btn.clicked.connect(self.add_goal)
        buttons_layout.addWidget(add_btn)
        
        delete_btn = QPushButton("Delete Goal")
        delete_btn.clicked.connect(self.delete_goal)
        buttons_layout.addWidget(delete_btn)
        
        toggle_btn = QPushButton("Toggle Complete")
        toggle_btn.clicked.connect(self.toggle_goal_complete)
        buttons_layout.addWidget(toggle_btn)
        
        layout.addLayout(buttons_layout)
        
        widget.setLayout(layout)
        return widget
    
    def refresh_goals_list(self):
        self.goals_list.clear()
        
        # Získej goals pro aktuální cyklus
        current_goals = self.parent_window.get_current_cycle_goals()
        
        for goal in current_goals:
            # goal = [name, subclass, timer, score, start, checked, end, completed]
            name = goal[0]
            subclass = goal[1]
            timer = goal[2]
            score = goal[3]
            checked = goal[5] if len(goal) > 5 else False
            
            # Vytvoř text
            check_mark = "☑" if checked else "☐"
            text = f"{check_mark} {name} | {subclass} | {timer}h | score {score}"
            
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, goal)  # Ulož celý goal jako data
            self.goals_list.addItem(item)
    
    def add_goal(self):
        # Zavolá SetGoalsDialog
        self.parent_window.show_goals_dialog()
        self.refresh_goals_list()
    
    def delete_goal(self):
        current_item = self.goals_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a goal to delete.")
            return
        
        # Získej goal data
        goal = current_item.data(Qt.UserRole)
        
        # Potvrzení
        reply = QMessageBox.question(
            self,
            "Delete Goal",
            f"Are you sure you want to delete:\n{goal[0]}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Smaž z listu
            self.goal.list_of_all_goal_objects.remove(goal)
            self.goal.update_data_frame()
            self.refresh_goals_list()
            print(f"✅ Goal deleted: {goal[0]}")
    
    def toggle_goal_complete(self):
        current_item = self.goals_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a goal.")
            return
        
        # Získej goal data
        goal = current_item.data(Qt.UserRole)
        
        # Toggle checked (index 5)
        if len(goal) > 5:
            goal[5] = not goal[5]
            self.goal.update_data_frame()
            self.refresh_goals_list()
            
            status = "completed" if goal[5] else "uncompleted"
            print(f"✅ Goal marked as {status}: {goal[0]}")
    
    # ===== TASKS TAB =====
    def create_tasks_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        info_label = QLabel("All Tasks")
        info_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(info_label)
        
        # List widget
        self.tasks_list = QListWidget()
        self.refresh_tasks_list()
        layout.addWidget(self.tasks_list)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        delete_btn = QPushButton("Delete Task")
        delete_btn.clicked.connect(self.delete_task)
        buttons_layout.addWidget(delete_btn)
        
        layout.addLayout(buttons_layout)
        
        widget.setLayout(layout)
        return widget
    
    def refresh_tasks_list(self):
        self.tasks_list.clear()
        
        for task in self.all_tasks.list_of_all_tasks_objects:
            # task = [name, subclass, date, hours, score, review]
            name = task[0]
            subclass = task[1]
            date = task[2]
            hours = task[3]
            
            date_str = date.strftime("%d.%m.%Y") if isinstance(date, datetime) else str(date)
            text = f"{name} | {subclass} | {date_str} | {hours}h"
            
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, task)
            self.tasks_list.addItem(item)
    
    def delete_task(self):
        current_item = self.tasks_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a task to delete.")
            return
        
        task = current_item.data(Qt.UserRole)
        
        reply = QMessageBox.question(
            self,
            "Delete Task",
            f"Delete task:\n{task[0]}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.all_tasks.list_of_all_tasks_objects.remove(task)
            self.all_tasks.update_data_frame()
            self.refresh_tasks_list()
            print(f"✅ Task deleted: {task[0]}")
    
    # ===== REWARDS TAB =====
    def create_rewards_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        info_label = QLabel("All Rewards")
        info_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(info_label)
        
        self.rewards_list = QListWidget()
        self.refresh_rewards_list()
        layout.addWidget(self.rewards_list)
        
        buttons_layout = QHBoxLayout()
        
        delete_btn = QPushButton("Delete Reward")
        delete_btn.clicked.connect(self.delete_reward)
        buttons_layout.addWidget(delete_btn)
        
        toggle_btn = QPushButton("Toggle Finished")
        toggle_btn.clicked.connect(self.toggle_reward_finished)
        buttons_layout.addWidget(toggle_btn)
        
        layout.addLayout(buttons_layout)
        
        widget.setLayout(layout)
        return widget
    
    def refresh_rewards_list(self):
        self.rewards_list.clear()
        
        for reward in self.reward.list_of_all_reward_objects:
            # reward = [date, name, time, finished]
            date = reward[0]
            name = reward[1]
            time = reward[2]
            finished = reward[3]
            
            date_str = date.strftime("%d.%m.%Y") if isinstance(date, datetime) else str(date)
            icon = "✅" if finished else "🎁"
            text = f"{icon} {name} | {date_str} | {time}h"
            
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, reward)
            self.rewards_list.addItem(item)
    
    def delete_reward(self):
        current_item = self.rewards_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a reward.")
            return
        
        reward = current_item.data(Qt.UserRole)
        
        reply = QMessageBox.question(
            self,
            "Delete Reward",
            f"Delete reward:\n{reward[1]}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.reward.list_of_all_reward_objects.remove(reward)
            self.reward.update_data_frame()
            self.refresh_rewards_list()
            print(f"✅ Reward deleted: {reward[1]}")
    
    def toggle_reward_finished(self):
        current_item = self.rewards_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a reward.")
            return
        
        reward = current_item.data(Qt.UserRole)
        reward[3] = not reward[3]
        self.reward.update_data_frame()
        self.refresh_rewards_list()
        
        status = "finished" if reward[3] else "unfinished"
        print(f"✅ Reward marked as {status}: {reward[1]}")
    
    # ===== NOTES TAB =====
    def create_notes_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        info_label = QLabel("All Notes")
        info_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(info_label)
        
        self.notes_list = QListWidget()
        self.refresh_notes_list()
        layout.addWidget(self.notes_list)
        
        buttons_layout = QHBoxLayout()
        
        delete_btn = QPushButton("Delete Note")
        delete_btn.clicked.connect(self.delete_note)
        buttons_layout.addWidget(delete_btn)
        
        layout.addLayout(buttons_layout)
        
        widget.setLayout(layout)
        return widget
    
    def refresh_notes_list(self):
        self.notes_list.clear()
        
        for note in self.note.list_of_all_notes_objects:
            # note = [date, subclass, topic, text]
            date = note[0]
            subclass = note[1]
            topic = note[2]
            
            date_str = date.strftime("%d.%m.%Y") if isinstance(date, datetime) else str(date)
            text = f"📝 {topic} | {subclass} | {date_str}"
            
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, note)
            self.notes_list.addItem(item)
    
    def delete_note(self):
        current_item = self.notes_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a note.")
            return
        
        note = current_item.data(Qt.UserRole)
        
        reply = QMessageBox.question(
            self,
            "Delete Note",
            f"Delete note:\n{note[2]}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.note.list_of_all_notes_objects.remove(note)
            self.note.update_data_frame()
            self.refresh_notes_list()
            print(f"✅ Note deleted: {note[2]}")
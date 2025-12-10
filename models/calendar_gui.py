# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QCalendarWidget, QLabel, QPushButton, QListWidget, QListWidgetItem,
    QDialog, QLineEdit, QTextEdit, QSpinBox, QComboBox, QFormLayout,
    QMessageBox, QTabWidget, QScrollArea, QGridLayout, QFrame,
    QSplitter, QGroupBox
)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette, QTextCharFormat


class TaskDialog(QDialog):
    """Dialog for adding/editing tasks"""
    def __init__(self, parent=None, task_data=None, subclasses=None):
        super().__init__(parent)
        self.setWindowTitle("Add Task" if task_data is None else "Edit Task")
        self.setMinimumWidth(500)
        self.task_data = task_data
        self.subclasses = subclasses or []

        self.setup_ui()

        if task_data:
            self.load_task_data(task_data)

    def setup_ui(self):
        layout = QFormLayout()

        # Task name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter task name")
        layout.addRow("Task Name:", self.name_input)

        # Subclass (category)
        self.subclass_combo = QComboBox()
        self.subclass_combo.setEditable(True)
        self.subclass_combo.addItems(self.subclasses)
        self.subclass_combo.setPlaceholderText("Select or enter category")
        layout.addRow("Category:", self.subclass_combo)

        # Date
        self.date_edit = QCalendarWidget()
        self.date_edit.setGridVisible(True)
        self.date_edit.setSelectedDate(QDate.currentDate())
        layout.addRow("Date:", self.date_edit)

        # Desired time
        self.time_spin = QSpinBox()
        self.time_spin.setRange(0, 24)
        self.time_spin.setValue(1)
        self.time_spin.setSuffix(" hours")
        layout.addRow("Time to Spend:", self.time_spin)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")

        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addRow("", button_layout)

        self.setLayout(layout)

    def load_task_data(self, task_data):
        """Load existing task data into the form"""
        self.name_input.setText(task_data[0])
        self.subclass_combo.setCurrentText(task_data[1])
        self.time_spin.setValue(task_data[3])

    def get_task_data(self):
        """Return task data from the form"""
        task_date = self.date_edit.selectedDate().toPyDate()
        return [
            self.name_input.text(),
            self.subclass_combo.currentText(),
            task_date,
            self.time_spin.value(),
            None,  # score
            ["", "", ""]  # review [learnt, dont_understand, next_step]
        ]


class ReviewDialog(QDialog):
    """Dialog for reviewing/scoring tasks"""
    def __init__(self, parent=None, task_name=""):
        super().__init__(parent)
        self.setWindowTitle(f"Review Task: {task_name}")
        self.setMinimumWidth(500)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()

        # Score
        self.score_spin = QSpinBox()
        self.score_spin.setRange(0, 10)
        self.score_spin.setValue(5)
        self.score_spin.setSuffix(" / 10")
        layout.addRow("Score:", self.score_spin)

        # What I learned
        self.learnt_text = QTextEdit()
        self.learnt_text.setPlaceholderText("What did you learn?")
        self.learnt_text.setMaximumHeight(100)
        layout.addRow("Learnt:", self.learnt_text)

        # What I don't understand
        self.dont_understand_text = QTextEdit()
        self.dont_understand_text.setPlaceholderText("What don't you understand?")
        self.dont_understand_text.setMaximumHeight(100)
        layout.addRow("Don't Understand:", self.dont_understand_text)

        # Next steps
        self.next_step_text = QTextEdit()
        self.next_step_text.setPlaceholderText("What should be your next step?")
        self.next_step_text.setMaximumHeight(100)
        layout.addRow("Next Step:", self.next_step_text)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Review")
        self.cancel_btn = QPushButton("Cancel")

        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addRow("", button_layout)

        self.setLayout(layout)

    def get_review_data(self):
        """Return review data from the form"""
        return {
            'score': self.score_spin.value(),
            'learnt': self.learnt_text.toPlainText(),
            'dont_understand': self.dont_understand_text.toPlainText(),
            'next_step': self.next_step_text.toPlainText()
        }


class GoalDialog(QDialog):
    """Dialog for adding goals"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add 12-Week Goal")
        self.setMinimumWidth(500)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()

        # Goal name
        self.goal_input = QLineEdit()
        self.goal_input.setPlaceholderText("What's your 12-week goal?")
        layout.addRow("Goal:", self.goal_input)

        # Subclass
        self.subclass_input = QLineEdit()
        self.subclass_input.setPlaceholderText("Category/sorting name")
        layout.addRow("Category:", self.subclass_input)

        # Timer (total hours)
        self.timer_spin = QSpinBox()
        self.timer_spin.setRange(1, 1000)
        self.timer_spin.setValue(50)
        self.timer_spin.setSuffix(" hours")
        layout.addRow("Total Time Budget:", self.timer_spin)

        # Average score threshold
        self.score_spin = QSpinBox()
        self.score_spin.setRange(1, 10)
        self.score_spin.setValue(7)
        self.score_spin.setSuffix(" / 10")
        layout.addRow("Target Avg Score:", self.score_spin)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Goal")
        self.cancel_btn = QPushButton("Cancel")

        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addRow("", button_layout)

        self.setLayout(layout)

    def get_goal_data(self):
        """Return goal data from the form"""
        return [
            self.goal_input.text(),
            self.subclass_input.text(),
            self.timer_spin.value(),
            self.score_spin.value(),
            datetime.now()
        ]


class CalendarGUI(QMainWindow):
    """Main calendar-style GUI for 12-week app"""

    def __init__(self, allTasks, goal, addiction, note, reward, filter_file):
        super().__init__()

        # Store references to data models
        self.allTasks = allTasks
        self.goal = goal
        self.addiction = addiction
        self.note = note
        self.reward = reward
        self.filter_file = filter_file

        self.setWindowTitle("12 Week Year - Task & Goal Tracker")
        self.setGeometry(100, 100, 1400, 900)

        self.setup_ui()
        self.load_tasks()

    def setup_ui(self):
        """Setup the main user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout - horizontal split
        main_layout = QHBoxLayout()

        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Horizontal)

        # Left side: Calendar and tasks for selected date
        left_widget = self.create_calendar_section()

        # Right side: Goals, upcoming tasks, and stats
        right_widget = self.create_sidebar_section()

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)

        # Apply styling
        self.apply_styling()

    def create_calendar_section(self):
        """Create the calendar and task list section"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Header with title
        header = QLabel("📅 Calendar View")
        header.setFont(QFont("Arial", 18, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumHeight(350)
        self.calendar.clicked.connect(self.date_selected)
        layout.addWidget(self.calendar)

        # Selected date label
        self.selected_date_label = QLabel(f"Tasks for: {QDate.currentDate().toString('dddd, MMMM d, yyyy')}")
        self.selected_date_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(self.selected_date_label)

        # Task list for selected date
        self.task_list = QListWidget()
        self.task_list.setMinimumHeight(200)
        self.task_list.itemDoubleClicked.connect(self.review_task)
        layout.addWidget(self.task_list)

        # Action buttons
        button_layout = QHBoxLayout()

        self.add_task_btn = QPushButton("➕ Add Task")
        self.add_task_btn.clicked.connect(self.add_task_dialog)

        self.remove_task_btn = QPushButton("❌ Remove Task")
        self.remove_task_btn.clicked.connect(self.remove_task)

        self.review_task_btn = QPushButton("⭐ Review Task")
        self.review_task_btn.clicked.connect(self.review_task)

        button_layout.addWidget(self.add_task_btn)
        button_layout.addWidget(self.remove_task_btn)
        button_layout.addWidget(self.review_task_btn)

        layout.addLayout(button_layout)

        widget.setLayout(layout)
        return widget

    def create_sidebar_section(self):
        """Create the sidebar with goals and stats"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Tab widget for different sections
        tabs = QTabWidget()

        # Goals tab
        goals_tab = self.create_goals_tab()
        tabs.addTab(goals_tab, "🎯 Goals")

        # All tasks tab
        all_tasks_tab = self.create_all_tasks_tab()
        tabs.addTab(all_tasks_tab, "📋 All Tasks")

        # Notes tab
        notes_tab = self.create_notes_tab()
        tabs.addTab(notes_tab, "📝 Notes")

        # Rewards tab
        rewards_tab = self.create_rewards_tab()
        tabs.addTab(rewards_tab, "🎁 Rewards")

        layout.addWidget(tabs)
        widget.setLayout(layout)
        return widget

    def create_goals_tab(self):
        """Create the goals management tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Header
        header = QLabel("Your 12-Week Goals")
        header.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(header)

        # Goals list
        self.goals_list = QListWidget()
        self.goals_list.setMinimumHeight(300)
        layout.addWidget(self.goals_list)

        # Goal buttons
        goal_btn_layout = QHBoxLayout()

        self.add_goal_btn = QPushButton("➕ Add Goal")
        self.add_goal_btn.clicked.connect(self.add_goal_dialog)

        self.remove_goal_btn = QPushButton("❌ Remove Goal")
        self.remove_goal_btn.clicked.connect(self.remove_goal)

        goal_btn_layout.addWidget(self.add_goal_btn)
        goal_btn_layout.addWidget(self.remove_goal_btn)

        layout.addLayout(goal_btn_layout)

        # Stats section
        stats_group = QGroupBox("Statistics")
        stats_layout = QVBoxLayout()

        self.total_tasks_label = QLabel("Total Tasks: 0")
        self.completed_tasks_label = QLabel("Completed: 0")
        self.avg_score_label = QLabel("Average Score: N/A")

        stats_layout.addWidget(self.total_tasks_label)
        stats_layout.addWidget(self.completed_tasks_label)
        stats_layout.addWidget(self.avg_score_label)

        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        widget.setLayout(layout)
        return widget

    def create_all_tasks_tab(self):
        """Create tab showing all tasks"""
        widget = QWidget()
        layout = QVBoxLayout()

        header = QLabel("All Tasks Overview")
        header.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(header)

        self.all_tasks_list = QListWidget()
        layout.addWidget(self.all_tasks_list)

        widget.setLayout(layout)
        return widget

    def create_notes_tab(self):
        """Create notes tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        header = QLabel("Notes")
        header.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(header)

        self.notes_list = QListWidget()
        layout.addWidget(self.notes_list)

        # Add note button
        add_note_btn = QPushButton("➕ Add Note")
        add_note_btn.clicked.connect(self.add_note_dialog)
        layout.addWidget(add_note_btn)

        widget.setLayout(layout)
        return widget

    def create_rewards_tab(self):
        """Create rewards tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        header = QLabel("Rewards")
        header.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(header)

        self.rewards_list = QListWidget()
        layout.addWidget(self.rewards_list)

        # Add reward button
        add_reward_btn = QPushButton("➕ Add Reward")
        add_reward_btn.clicked.connect(self.add_reward_dialog)
        layout.addWidget(add_reward_btn)

        widget.setLayout(layout)
        return widget

    def apply_styling(self):
        """Apply modern styling to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: black;
            }
            QCalendarWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QGroupBox {
                border: 2px solid #ddd;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

    def load_tasks(self):
        """Load tasks from data model"""
        self.update_calendar_highlights()
        self.update_task_list_for_date()
        self.update_goals_list()
        self.update_all_tasks_list()
        self.update_notes_list()
        self.update_rewards_list()
        self.update_statistics()

    def update_calendar_highlights(self):
        """Highlight dates that have tasks"""
        # Clear previous formats
        default_format = QTextCharFormat()

        # Highlight format for dates with tasks
        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QColor(144, 238, 144))  # Light green

        # Get all task dates
        for task in self.allTasks.list_of_all_tasks_objects:
            task_date = task[2]
            if isinstance(task_date, str):
                try:
                    task_date = datetime.strptime(task_date, "%Y-%m-%d").date()
                except:
                    continue

            qdate = QDate(task_date.year, task_date.month, task_date.day)
            self.calendar.setDateTextFormat(qdate, highlight_format)

    def date_selected(self, qdate):
        """Handle date selection in calendar"""
        self.selected_date_label.setText(f"Tasks for: {qdate.toString('dddd, MMMM d, yyyy')}")
        self.update_task_list_for_date()

    def update_task_list_for_date(self):
        """Update task list for the selected date"""
        self.task_list.clear()

        selected_date = self.calendar.selectedDate().toPyDate()

        for idx, task in enumerate(self.allTasks.list_of_all_tasks_objects):
            task_date = task[2]
            if isinstance(task_date, str):
                try:
                    task_date = datetime.strptime(task_date, "%Y-%m-%d").date()
                except:
                    continue

            if task_date == selected_date:
                task_name = task[0]
                task_category = task[1]
                task_hours = task[3]
                task_score = task[4]

                # Format task display
                score_text = f"⭐ {task_score}/10" if task_score is not None else "⚪ Not reviewed"
                item_text = f"{task_name} [{task_category}] - {task_hours}h - {score_text}"

                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, idx)  # Store task index
                self.task_list.addItem(item)

    def update_goals_list(self):
        """Update the goals list"""
        self.goals_list.clear()

        for idx, goal in enumerate(self.goal.list_of_all_goals_objects):
            goal_name = goal[0]
            goal_category = goal[1]
            goal_timer = goal[2]
            goal_target = goal[3]

            item_text = f"🎯 {goal_name} [{goal_category}]\n   ⏱️ {goal_timer}h remaining | Target: {goal_target}/10"

            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, idx)
            self.goals_list.addItem(item)

    def update_all_tasks_list(self):
        """Update the all tasks list"""
        self.all_tasks_list.clear()

        for idx, task in enumerate(self.allTasks.list_of_all_tasks_objects):
            task_name = task[0]
            task_date = task[2]
            task_score = task[4]

            score_text = f"⭐ {task_score}/10" if task_score is not None else "⚪"
            item_text = f"{score_text} {task_name} - {task_date}"

            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, idx)
            self.all_tasks_list.addItem(item)

    def update_notes_list(self):
        """Update the notes list"""
        self.notes_list.clear()

        if hasattr(self.note, 'list_of_all_notes_objects'):
            for note in self.note.list_of_all_notes_objects:
                note_date = note[0]
                note_topic = note[2]
                item_text = f"📝 {note_topic} - {note_date}"
                self.notes_list.addItem(item_text)

    def update_rewards_list(self):
        """Update the rewards list"""
        self.rewards_list.clear()

        if hasattr(self.reward, 'list_of_all_rewards_objects'):
            for reward in self.reward.list_of_all_rewards_objects:
                reward_text = reward[1]
                reward_time = reward[2]
                reward_done = reward[3]

                status = "✅" if reward_done else "⚪"
                item_text = f"{status} {reward_text} ({reward_time}h)"
                self.rewards_list.addItem(item_text)

    def update_statistics(self):
        """Update statistics display"""
        total_tasks = len(self.allTasks.list_of_all_tasks_objects)
        completed_tasks = sum(1 for task in self.allTasks.list_of_all_tasks_objects if task[4] is not None)

        # Calculate average score
        scores = [task[4] for task in self.allTasks.list_of_all_tasks_objects if task[4] is not None]
        avg_score = sum(scores) / len(scores) if scores else 0

        self.total_tasks_label.setText(f"Total Tasks: {total_tasks}")
        self.completed_tasks_label.setText(f"Completed: {completed_tasks}")
        self.avg_score_label.setText(f"Average Score: {avg_score:.1f}/10" if avg_score > 0 else "Average Score: N/A")

    def add_task_dialog(self):
        """Show dialog to add a new task"""
        # Get existing subclasses for suggestions
        subclasses = list(set([task[1] for task in self.allTasks.list_of_all_tasks_objects if task[1]]))

        dialog = TaskDialog(self, subclasses=subclasses)

        if dialog.exec_() == QDialog.Accepted:
            task_data = dialog.get_task_data()
            self.allTasks.add_new_task(task_data)
            self.load_tasks()
            QMessageBox.information(self, "Success", "Task added successfully!")

    def remove_task(self):
        """Remove selected task"""
        current_item = self.task_list.currentItem()

        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a task to remove")
            return

        task_idx = current_item.data(Qt.UserRole)
        task_name = self.allTasks.list_of_all_tasks_objects[task_idx][0]

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{task_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.allTasks.remove_task_df(task_idx)
            self.load_tasks()
            QMessageBox.information(self, "Success", "Task removed successfully!")

    def review_task(self, item=None):
        """Show dialog to review a task"""
        if item is None:
            item = self.task_list.currentItem()

        if not item:
            QMessageBox.warning(self, "Warning", "Please select a task to review")
            return

        task_idx = item.data(Qt.UserRole)
        task = self.allTasks.list_of_all_tasks_objects[task_idx]
        task_name = task[0]

        dialog = ReviewDialog(self, task_name)

        if dialog.exec_() == QDialog.Accepted:
            review_data = dialog.get_review_data()

            self.allTasks.setting_task(
                task_idx,
                review_data['score'],
                review_data['learnt'],
                review_data['dont_understand'],
                review_data['next_step']
            )

            # Update timer if goal exists
            self.goal.upadating_timer(task_idx, task[3])

            self.load_tasks()
            QMessageBox.information(self, "Success", "Task reviewed successfully!")

    def add_goal_dialog(self):
        """Show dialog to add a new goal"""
        dialog = GoalDialog(self)

        if dialog.exec_() == QDialog.Accepted:
            goal_data = dialog.get_goal_data()
            self.goal.add_goal(goal_data)
            self.load_tasks()
            QMessageBox.information(self, "Success", "Goal added successfully!")

    def remove_goal(self):
        """Remove selected goal"""
        current_item = self.goals_list.currentItem()

        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a goal to remove")
            return

        goal_idx = current_item.data(Qt.UserRole)
        goal_name = self.goal.list_of_all_goals_objects[goal_idx][0]

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete goal '{goal_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.goal.removing_timer(goal_idx)
            self.load_tasks()
            QMessageBox.information(self, "Success", "Goal removed successfully!")

    def add_note_dialog(self):
        """Add a note (simplified version)"""
        QMessageBox.information(self, "Coming Soon", "Note creation dialog - to be implemented")

    def add_reward_dialog(self):
        """Add a reward (simplified version)"""
        QMessageBox.information(self, "Coming Soon", "Reward creation dialog - to be implemented")

    def closeEvent(self, event):
        """Save data when closing the application"""
        self.allTasks.save_data_frame()
        event.accept()


def main():
    """Main function to run the calendar GUI"""
    from models.all_tasks import All_tasks
    from models.goal import Goal
    from models.addiction import Addiction
    from models.notes_class import Note
    from models.reward import Reward
    from models.filters import Filter

    app = QApplication(sys.argv)

    # Initialize data models
    allTasks = All_tasks()
    addiction = Addiction()
    note = Note()
    reward_obj = Reward()
    goal = Goal(allTasks)
    filter_file = Filter(allTasks)

    # Create and show main window
    window = CalendarGUI(allTasks, goal, addiction, note, reward_obj, filter_file)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

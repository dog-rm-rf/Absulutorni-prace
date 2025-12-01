from PyQt5 import QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt


# Create the application - this is the "engine" we talked about
app = QApplication(sys.argv) #setup
# Create the main window - this is your "house"
window = QMainWindow()
window.setGeometry(100, 100, 800, 600)
window.setWindowTitle("12 week")


# Create a central widget to hold everything
central_widget = QWidget()
window.setCentralWidget(central_widget)

# Create a vertical layout (things stacked top to bottom)
main_layout = QVBoxLayout()
central_widget.setLayout(main_layout)

# Create labels - these display text
week_label = QLabel("Week 1")
week_label.setAlignment(Qt.AlignCenter)  # Center the text

# Create a horizontal layout for day names (things side by side)
days_layout = QHBoxLayout()

# Create labels for each day
day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_labels = []

for day in day_names:
    label = QLabel(day)
    label.setAlignment(Qt.AlignCenter)
    day_labels.append(label)
    days_layout.addWidget(label)

# Add everything to the main layout
main_layout.addWidget(week_label)
main_layout.addLayout(days_layout)

# Show the window
window.show()

# Start the event loop - "start the engine"
sys.exit(app.exec_())



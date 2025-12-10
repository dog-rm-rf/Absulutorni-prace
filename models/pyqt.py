import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QApplication, QLabel, QMainWindow, QMenu, QCheckBox
from PyQt5.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("My App")

        widget = QCheckBox("This is a checkbox")
        widget.setCheckState(Qt.Checked)


        widget.stateChanged.connect(self.show_state)

        
        # widget = QLabel("Hola")
        # widget.setPixmap(QPixmap("/home/vojtasek/3542.webp"))
        # widget.setScaledContents(True)

        # font = widget.font()
        # font.setPointSize(50)
        # widget.setFont(font)
        # align_top_left = Qt.AlignLeft | Qt.AlignTop
        # widget.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        
        self.setCentralWidget(widget)
    def show_state(self, s):
        print(s == Qt.Checked)
        print(s)



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
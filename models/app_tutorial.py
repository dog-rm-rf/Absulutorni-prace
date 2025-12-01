import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


# Subclass QMainWindow to customize your application's main window, MainWindow is child, Qmainwindow is parent, child inherits from parent
class MainWindow(QMainWindow):
    #self. give you access to the MainWindow and the QMainWindow class
    def __init__(self):
        #super gives access to parent class QMainWindow so if there is some function
        #super runs the init code in QMainWindow
        #also could QMainWindow.__init__(self)
        #Use super() ONLY when you're overriding a method:
        super().__init__()

        self.button_is_checked = True

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")
        button.setCheckable(True)# Button can toggle on/off
        button.clicked.connect(self.the_button_was_clicked) #just passes the function like phone number, with () we are running the function now and using the return value 
        #when we click we toggle the states so in this case from true to false
        button.clicked.connect(self.the_button_was_toggled) # Wire up second function
        
        #we set the state, true
        button.setChecked(self.button_is_checked)
        self.setFixedSize(QSize(400, 300))

        self.button.released.connect(self.the_button_was_released)
        self.button.setChecked(self.button_is_checked)


        # Set the central widget of the Window.
        self.setCentralWidget(button)
        

    def the_button_was_clicked(self):
        print("Clicked!")

    def the_button_was_toggled(self, checked):
        self.button_is_checked = checked

        print(self.button_is_checked)
    # def the_button_was_toggled(self, checked):
    #     print("Checked?", checked)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
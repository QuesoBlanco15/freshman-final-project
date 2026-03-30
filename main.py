import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel
from PyQt6.QtGui import QColor, QPalette
from d20dice import roll_dice


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Background
        self.setStyleSheet("""
                            QMainWindow {
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 #0d0d0d, stop: 1 #1c1c1c
        );
        color: white;
    }
                           """)

        self.setWindowTitle("John DnD")

        # Test Button
        self.button = QPushButton("Press to Roll")
        self.button.setFixedSize(100, 50)
        self.button.clicked.connect(self.dicerolltest)
        

        # Set the central widget of the Window.
        self.setCentralWidget(self.button)
    
    def dicerollD20(self):
        roll = str(roll_dice(20))
        self.button.setText(roll)
    
    


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
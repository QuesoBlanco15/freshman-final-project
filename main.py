import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QSplitter, QVBoxLayout
from diceClass import *
from views import *


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

        # Set the central widget of the Window.
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Sidebar View
        sidebar = SidebarView()

        # Character Sheet View
        characterSheet = CharacterSheetView()

        # Dice View
        dice = DiceView()

        # Dice Multipliers/stats view (?)
        multipliers = MultiplierView()

         # Right side splits
        right_side = QSplitter(Qt.Orientation.Vertical)
        right_side.addWidget(dice)
        right_side.addWidget(multipliers)
        right_side.setSizes([600, 600])

        main_view = QSplitter(Qt.Orientation.Horizontal)
        main_view.addWidget(sidebar)
        main_view.addWidget(characterSheet)
        main_view.addWidget(right_side)
        main_view.setSizes([85, 400, 600])

        layout.addWidget(main_view)

    
    


app = QApplication(sys.argv)

window = MainWindow()
window.showMaximized()

app.exec()
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel, QSplitter, QVBoxLayout, QFrame, QListWidget, QTextEdit
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

        # Set the central widget of the Window.
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Sidebar View
        sidebar = QFrame()
        sidebar.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.addWidget(QLabel("Sidebar"))
        sidebar_layout.addWidget(QListWidget())

        # Character Sheet View
        content = QFrame()
        content.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        content_layout = QVBoxLayout(content)
        content_layout.addWidget(QLabel("Main Content"))
        content_layout.addWidget(QTextEdit())

        # Dice View
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.button = QPushButton("Press to Roll")
        self.button.setFixedSize(100, 50)
        self.button.clicked.connect(self.dicerollD20)
        panel_layout = QVBoxLayout(panel)
        panel_layout.addWidget(QLabel("Details Panel"))
        panel_layout.addWidget(self.button)
        # Attempt to make multiple buttons labeled d12, d10, d8, and d4 (please) -cole

         # Dice Multiplier/effect view (?)
        frame4 = QFrame()
        frame4.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        frame4_layout = QVBoxLayout(frame4)
        frame4_layout.addWidget(QLabel("Frame 4"))
        frame4_layout.addWidget(QTextEdit())

         # Right side splits
        right_side = QSplitter(Qt.Orientation.Vertical)
        right_side.addWidget(panel)
        right_side.addWidget(frame4)
        right_side.setSizes([600, 600])

        main_view = QSplitter(Qt.Orientation.Horizontal)
        main_view.addWidget(sidebar)
        main_view.addWidget(content)
        main_view.addWidget(right_side)
        main_view.setSizes([85, 400, 600])

        layout.addWidget(main_view)

    def dicerollD20(self):
        roll = str(roll_dice(20))
        self.button.setText(roll)

    
    


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
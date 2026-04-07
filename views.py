
from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QFrame, QListWidget, QTextEdit
from d20dice import roll_dice

# Sidebar View
    # TO DO
        # Add Settings
        # Add Characters
        # Add an Add Characters
class SidebarView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)

        sidebar_layout = QVBoxLayout(self)
        sidebar_layout.addWidget(QLabel("Sidebar"))
        sidebar_layout.addWidget(QListWidget())

# Character Sheet View
    # TO DO
        # Add ability to change with change of character
        # Add Import Sheet (?) 
        # Lokey don't know what else
class CharacterSheetView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)

        content_layout = QVBoxLayout(self)
        content_layout.addWidget(QLabel("Main Content"))
        content_layout.addWidget(QTextEdit())

# Dice View
    # TO DO
        # Add Multiple Dice (d20, d12, d10, d8, d4)
        # Add Drag to roll maybe
        # Add Awesome Animations
class DiceView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)

        self.button = QPushButton("Press to Roll")
        self.button.setFixedSize(100, 50)
        self.button.clicked.connect(self.dicerollD20)
        panel_layout = QVBoxLayout(self)
        panel_layout.addWidget(QLabel("Details Panel"))
        panel_layout.addWidget(self.button)

    def dicerollD20(self):
        roll = str(roll_dice(20))
        self.button.setText(roll)

# Multiplier View
    # TO DO
        # Genuinely don't know what the heck is happening in this box so someone add pls
class MultiplierView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)

        frame4_layout = QVBoxLayout(self)
        frame4_layout.addWidget(QLabel("Frame 4"))
        frame4_layout.addWidget(QTextEdit())

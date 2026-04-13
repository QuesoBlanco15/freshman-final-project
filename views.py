
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QFrame, QListWidget, QTextEdit, QComboBox, QWidget,QScrollArea
from diceClass import *
from widgets import *

# Sidebar View
    # TO DO
        # Add Settings
        # Add Characters
        # Add an Add Characters
    #added by Andre:
        # a character selection/creation/deletion that will be inside of the sidebar
        # A widget that adds a new Character to the bar if clicked
class SidebarView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        sidebar_layout = QVBoxLayout(self)
        scroll = QScrollArea() 
        scroll.setWidgetResizable(True) 
        character = QWidget() 
        character_layout = QVBoxLayout(character) 
        scroll.setWidget(character)

        
        character_layout = QVBoxLayout()
        self.settings = QPushButton()
        self.settings.setIcon(QIcon("icons/setting-lines.png"))
        self.settings.setIconSize(QSize(25, 25))
        self.settings.clicked.connect(self.show_settings)
        

        add_char_btn = QPushButton("add")
        add_char_btn.setFixedWidth(50)
        add_char_btn.clicked.connect(lambda:self.add_new_character(character_layout))

        sidebar_layout.addWidget(scroll)
        sidebar_layout.addLayout(character_layout)
        sidebar_layout.addWidget(self.settings)
        character_layout.addWidget(add_char_btn)
        character_layout.addStretch()

    def add_new_character(self,character_layout):
        count = 0
        for i in range(character_layout.count()):
            item = character_layout.itemAt(i)
            if item.widget() is not None:
                count+=1
        char_name = str(count)
        new_char = QPushButton(char_name)
        new_char.setFixedWidth(50)
        character_layout.insertWidget(count-1,new_char)

    def show_settings(self, checked):
        self.w = SettingsWidget()
        self.w.show()


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
        self.setCursor(Qt.CursorShape.OpenHandCursor)

    
        self.dice = DiceWidget(self)

        self.dice_select = QComboBox(self)
        self.dice_select.addItems(["d4", "d6", "d8", "d10", "d12", "d20"])
        self.dice_select.setCurrentText("d20")
        self.dice_select.currentTextChanged.connect(
            lambda text: self.dice.set_dice(int(text[1:]))
        )

        panel_layout = QVBoxLayout(self)
        panel_layout.addWidget(self.dice)
        panel_layout.addWidget(self.dice_select)

    def diceroll(self):
        die = Dice(self.die_type)
        roll = str(die.roll_dice())
        self.button.setText(roll)

        

# Multiplier View
    # TO DO
        # Genuinely don't know what the heck is happening in this box so someone add pls
class MultiplierView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)

        multiplier_layout = QVBoxLayout(self)
        multiplier_layout.addWidget(QLabel("Multiplier View"))
        multiplier_layout.addWidget(QTextEdit())

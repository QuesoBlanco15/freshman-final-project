
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QFrame, QListWidget, QTextEdit, QComboBox, QWidget , QStackedLayout
from d20dice import roll_dice

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
        character_layout = QVBoxLayout()
        settings = QPushButton()
        settings.setIcon(QIcon("icons/setting-lines.png"))
        settings.setIconSize(QSize(25, 25))

        add_char_btn = QPushButton("add")
        add_char_btn.clicked.connect(lambda:self.add_new_character(character_layout))

        sidebar_layout.addLayout(character_layout)
        sidebar_layout.addWidget(settings)
        character_layout.addWidget(add_char_btn)

    def add_new_character(self,character_layout):
        count = 0
        for i in range(character_layout.count()):
            item = character_layout.itemAt(i)
            if item.widget() is not None:
                count+=1
        char_name = str(count)
        new_char = QPushButton(char_name)
        character_layout.addWidget(new_char)


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

        # Dice State
        self.die_type = 20

        self.button = QPushButton("Press to Roll")
        self.button.setFixedSize(100, 50)
        self.button.clicked.connect(self.diceroll)

        self.dice_select = QComboBox(self)
        self.dice_select.addItems(["d4", "d8", "d10", "d12", "d20"])
        self.dice_select.setCurrentText("d20")
        self.dice_select.currentTextChanged.connect(
            lambda text: self.setdice(int(text[1:]))
        )

        panel_layout = QVBoxLayout(self)
        panel_layout.addWidget(QLabel("Dice View"))
        panel_layout.addWidget(self.button)
        panel_layout.addWidget(self.dice_select)

    def diceroll(self):
        roll = str(roll_dice(self.die_type))
        self.button.setText(roll)

    def setdice(self, sides: int):
        self.die_type = sides
        

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

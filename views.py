from PyQt6.QtGui import QIcon,QAction
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QFrame,  QTextEdit, QComboBox, QWidget,QScrollArea,QDialog,QFormLayout,QLineEdit,QDialogButtonBox, QMessageBox, QMenu, QWidgetAction
from diceClass import *
from widgets import *
from characterClass import Character


#global variables to show the current character on display
current_char = None
button_list = []
char_list = []

# Sidebar View
    # TO DO
        # Add Settings
        # Add Characters
    #added by Andre:
        # a character selection/creation/deletion that will be inside of the sidebar
        # A widget that adds a new Character to the bar if clicked
class SidebarView(QWidget):
    def __init__(self, character_sheet, parent=None):
        super().__init__(parent)
        self.character_sheet = character_sheet
        sidebar_layout = QVBoxLayout(self)
        scroll = QScrollArea() 
        scroll.setWidgetResizable(True) 
        character = QWidget() 
        character_layout = QVBoxLayout(character) 
        scroll.setWidget(character)

        
        
        self.settings = QPushButton()
        self.settings.setIcon(QIcon("icons/setting-lines.png"))
        self.settings.setIconSize(QSize(25, 25))
        self.settings.clicked.connect(self.show_settings)
        

        add_char_btn = QPushButton("add")
        add_char_btn.setFixedWidth(50)
        add_char_btn.clicked.connect(lambda:self.add_new_character(character_layout))

        sidebar_layout.addWidget(scroll)
        sidebar_layout.addWidget(self.settings)
        character_layout.addWidget(add_char_btn)
        character_layout.addStretch()

    # centered around the add character button and gives ability to delete and edit created characters
    def add_new_character(self,character_layout):
        global button_list
        global char_list
        global current_char
        dialog = CharacterCreationDialog()
        
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        data = dialog.get_data()
        
        
        obj = Character()
        obj.name = data["name"]
        obj.clas = data["clas"]
        obj.race = data["race"]
        obj.strength = data["strength"]
        obj.dexterity = data["dexterity"]
        obj.constitution = data["constitution"]
        obj.intel = data["intel"]
        obj.wisdom = data["wisdom"]
        obj.is_set = True
        char_list.append(obj)

        
        
        index = len(char_list) - 1
        new_char_btn = QPushButton(obj.name)
        new_char_btn.setFixedWidth(50)
        new_char_btn.clicked.connect(lambda _, i=index: self.set_display(i))
        new_char_btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        new_char_btn.customContextMenuRequested.connect(
            lambda pos,i = index,btn = new_char_btn: self.open_context_menu(pos,i,btn)
        )
        button_list.append(new_char_btn)

        insert_index = character_layout.count() - 1
        character_layout.insertWidget(insert_index - 1, new_char_btn)

    #creates and adds edit and delete to the context menu
    def open_context_menu(self,pos,index,btn):
        menu = QMenu(self)
        edit = QAction("Edit Character",self)
        menu.addAction(edit)
        edit.triggered.connect(lambda _, idx=index:self.edit_character(idx))
        delete = QAction("Delete Character",self)
        menu.addAction(delete)
        delete.triggered.connect(lambda _, idx=index, b=btn: self.delete_character(idx, b))
        menu.exec(btn.mapToGlobal(pos))

    #editing the character
    def edit_character(self,index):
        global char_list, button_list, current_char
        
        char = char_list[index]
        
        dialog = CharacterCreationDialog()
        
        
        
        dialog.setWindowTitle("Edit Character")
        dialog.name_input.setText(char.name)
        dialog.class_input.setText(char.clas)
        dialog.race_input.setText(char.race)
        dialog.strength_input.setText(str(char.strength))
        dialog.dexterity_input.setText(str(char.dexterity))
        dialog.constitution_input.setText(str(char.constitution))
        dialog.intel_input.setText(str(char.intel))
        dialog.wisdom_input.setText(str(char.wisdom))
        
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        
        data = dialog.get_data()
        char.name = data["name"]
        char.clas = data["clas"]
        char.race = data["race"]
        char.strength = int(data["strength"])
        char.dexterity = int(data["dexterity"])
        char.constitution = int(data["constitution"])
        char.intel = int(data["intel"])
        char.wisdom = int(data["wisdom"])

        button_list[index].setText(char.name)


        if current_char == char:
            self.character_sheet.update_display()



    #deleteing the character
    def delete_character(self, index, btn):
        global char_list, button_list, current_char
        deleted_char = char_list[index]
        char_list.pop(index)
        button_list.remove(btn)
        btn.setParent(None)

        if len(char_list) ==0 and current_char == deleted_char:
            current_char = None
            self.character_sheet.update_display()
        for i, butn in enumerate(button_list):
            butn.clicked.disconnect()
            butn.clicked.connect(lambda _, idx=i: self.set_display(idx))
            butn.customContextMenuRequested.disconnect()
            butn.customContextMenuRequested.connect(
                lambda pos,idx = i,btn = butn: self.open_context_menu(pos,idx,btn)
            )

            
    #sets the display of the character sheet to the selected character
    def set_display(self,count):
        global current_char
        global char_list
        current_char = char_list[count]


        self.character_sheet.update_display()

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
        global current_char
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.layout = QFormLayout(self)
        

        self.name_label = QLabel("No character selected")
        self.class_label = QLabel("")
        self.race_label = QLabel("")
        self.str_label = QLabel("")
        self.dex_label = QLabel("")
        self.con_label = QLabel("")
        self.int_label = QLabel("")
        self.wis_label = QLabel("")

        

        self.layout.addRow("Name:", self.name_label)
        self.layout.addRow("Class:", self.class_label)
        self.layout.addRow("Race:", self.race_label)
        self.layout.addRow("Strength:", self.str_label)
        self.layout.addRow("Dexterity:", self.dex_label)
        self.layout.addRow("Constitution:", self.con_label)
        self.layout.addRow("Intelligence:", self.int_label)
        self.layout.addRow("Wisdom:", self.wis_label)

        
    #updates the display to the selected character
    def update_display(self):
        global current_char
        if current_char is None:
            self.name_label.setText("No character selected")
            self.class_label.setText("")
            self.race_label.setText("")
            self.str_label.setText("")
            self.dex_label.setText("")
            self.con_label.setText("")
            self.int_label.setText("")
            self.wis_label.setText("")
            return
        self.name_label.setText(current_char.name)
        self.class_label.setText(current_char.clas)
        self.race_label.setText(current_char.race)
        self.str_label.setText(str(current_char.strength))
        self.dex_label.setText(str(current_char.dexterity))
        self.con_label.setText(str(current_char.constitution))
        self.int_label.setText(str(current_char.intel))
        self.wis_label.setText(str(current_char.wisdom))

        
#a pop up window to collect the data for the players characters
class CharacterCreationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
                            CharacterCreationDialog {
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 #0d0d0d, stop: 1 #1c1c1c
        );
        color: white;
    }
                           """)
        self.setWindowTitle("Character Creation")

        layout = QFormLayout()
        self.setLayout(layout)
        self.name_input = QLineEdit()
        self.class_input = QLineEdit()
        self.race_input = QLineEdit()
        self.strength_input = QLineEdit()
        self.dexterity_input = QLineEdit()
        self.constitution_input = QLineEdit()
        self.intel_input = QLineEdit()
        self.wisdom_input = QLineEdit()

        layout.addRow("Please enter your name:", self.name_input)
        layout.addRow("Please enter your class:", self.class_input)
        layout.addRow("Please enter your Race:", self.race_input)
        layout.addRow("Please enter your strength:", self.strength_input)
        layout.addRow("Please enter your dexterity:", self.dexterity_input)
        layout.addRow("Please enter your constitution:", self.constitution_input)
        layout.addRow("Please enter your intel:", self.intel_input)
        layout.addRow("Please enter your wisdom:", self.wisdom_input)

        button = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button.accepted.connect(self.accept)
        button.rejected.connect(self.reject)
        layout.addWidget(button)
        self.setLayout(layout)

    def get_data(self):
        return {"name":self.name_input.text(),
            "clas":self.class_input.text(),
            "race":self.race_input.text(),
            "strength":self.strength_input.text(),
            "dexterity":self.dexterity_input.text(),
            "constitution":self.constitution_input.text(),
            "intel":self.intel_input.text(),
            "wisdom":self.wisdom_input.text()}
    
    def accept(self):
        
        int_fields = {
            "Strength": self.strength_input,
            "Dexterity": self.dexterity_input,
            "Constitution": self.constitution_input,
            "Intelligence": self.intel_input,
            "Wisdom": self.wisdom_input
        }

        for label, widget in int_fields.items():
            text = widget.text().strip()
            if not text.isdigit():
                QMessageBox.warning(
                    self,
                    "Invalid Input",
                    f"{label} must be a whole number."
                )
                widget.setFocus()
                return
        super().accept()
        

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

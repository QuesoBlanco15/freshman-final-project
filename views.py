
from PyQt6.QtGui import QIcon, QAction, QFont
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QFrame, QListWidget, QTextEdit, QComboBox, QWidget, QScrollArea, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QMenu, QWidgetAction, QSplitter, QGridLayout
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
roll = 0     
die = Dice()
class SidebarView(QWidget):
    def __init__(self, character_sheet, on_open_settings=None, parent=None):
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
        self._on_open_settings = on_open_settings
        

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
        obj.charisma = data["charisma"]
        obj.lore = data["lore"]
        obj.is_set = True
        char_list.append(obj)

        
        
        index = len(char_list) - 1
        
        new_char_btn = QPushButton(obj.name[:4])
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
        dialog.charisma_input.setText(str(char.charisma))
        dialog.lore_input.setPlainText(char.lore or "")
        
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
        char.charisma = int(data["charisma"])
        char.lore = data["lore"]

        button_list[index].setText(char.name[:4])


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
        self.w = SettingsView()
        self.w.show()
        if self._on_open_settings:
            self._on_open_settings(self.w)

# Character Sheet View
    # TO DO
        # Add ability to change with change of character
        # Add Import Sheet (?) 
        # Lokey don't know what else
class CharacterSheetView(QFrame):
    character_changed = pyqtSignal(object)
    def __init__(self, parent=None):
        super().__init__(parent)
        global current_char
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.setStyleSheet("""
            CharacterSheetView {
                border: 2px solid #4B1414;
                border-radius: 4px;
            }
        """)
 
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(4)
 
        self.name_label = QLabel("No character selected")
        self.name_label.setFont(QFont("Inter", 22, QFont.Weight.Bold))
        self.name_label.setStyleSheet("color: #ffffff;")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
 
        identity_row = QHBoxLayout()
        identity_row.setSpacing(6)
 
        self.class_label = QLabel("")
        self.class_label.setFont(QFont("Inter", 11))
        self.class_label.setStyleSheet("color: #888888;")
        self.class_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
 
        dot = QLabel("·")
        dot.setStyleSheet("color: #444;")
        dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
 
        self.race_label = QLabel("")
        self.race_label.setFont(QFont("Inter", 11))
        self.race_label.setStyleSheet("color: #888888;")
        self.race_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
 
        identity_row.addStretch()
        identity_row.addWidget(self.class_label)
        identity_row.addWidget(dot)
        identity_row.addWidget(self.race_label)
        identity_row.addStretch()
 
        self.layout.addWidget(self.name_label)
        self.layout.addLayout(identity_row)
        self.layout.addSpacing(16)
 
        grid = QGridLayout()
        grid.setColumnStretch(0, 3)
        grid.setColumnStretch(1, 1)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(10)
 
        stat_defs = [
            ("Strength",     "str_label"),
            ("Dexterity",    "dex_label"),
            ("Constitution", "con_label"),
            ("Intelligence", "int_label"),
            ("Wisdom",       "wis_label"),
            ("Charisma",     "charisma_label"),
        ]
 
        for row, (display, attr) in enumerate(stat_defs):
            name_lbl = QLabel(display)
            name_lbl.setFont(QFont("Inter", 11))
            name_lbl.setStyleSheet("color: #777777;")
 
            val_lbl = QLabel("—")
            val_lbl.setFont(QFont("Inter", 12, QFont.Weight.Bold))
            val_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            val_lbl.setStyleSheet("color: #dddddd;")
 
            setattr(self, attr, val_lbl)
            grid.addWidget(name_lbl, row, 0)
            grid.addWidget(val_lbl,  row, 1)
 
        self.layout.addLayout(grid)
        self.layout.addSpacing(16)
 
        self.lore_label = QLabel("LORE")
        self.lore_label.setFont(QFont("Inter", 9, QFont.Weight.Bold))
        self.lore_label.setStyleSheet("color: #555555; letter-spacing: 1px;")
 
        self.lore_edit = QTextEdit()
        self.lore_edit.setPlaceholderText("Character backstory, history, personality...")
        self.lore_edit.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #e0d8c8;
                border: 1px solid #2a2a2a;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Georgia', serif;
                font-size: 12px;
            }
        """)
        self.lore_edit.textChanged.connect(self._save_lore)
 
        self.notes_label = QLabel("NOTES")
        self.notes_label.setFont(QFont("Inter", 9, QFont.Weight.Bold))
        self.notes_label.setStyleSheet("color: #555555; letter-spacing: 1px;")
 
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Session notes, inventory, reminders...")
        self.notes_edit.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #c8d8e0;
                border: 1px solid #2a2a2a;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Georgia', serif;
                font-size: 12px;
            }
        """)
        self.notes_edit.textChanged.connect(self._save_notes)
 
        self.layout.addWidget(self.lore_label)
        self.layout.addWidget(self.lore_edit, stretch=1)
        self.layout.addWidget(self.notes_label)
        self.layout.addWidget(self.notes_edit, stretch=1)
 
        
    #updates the display to the selected character
    def update_display(self):
        global current_char
        if current_char is None:
            self.name_label.setText("No character selected")
            self.class_label.setText("")
            self.race_label.setText("")
            self.str_label.setText("—")
            self.dex_label.setText("—")
            self.con_label.setText("—")
            self.int_label.setText("—")
            self.wis_label.setText("—")
            self.charisma_label.setText("—")
            self.lore_edit.blockSignals(True)
            self.lore_edit.setPlainText("")
            self.lore_edit.blockSignals(False)
            self.notes_edit.blockSignals(True)
            self.notes_edit.setPlainText("")
            self.notes_edit.blockSignals(False)
            self.character_changed.emit(None)
            return
        self.name_label.setText(current_char.name)
        self.class_label.setText(current_char.clas)
        self.race_label.setText(current_char.race)
        self.str_label.setText(str(current_char.strength))
        self.dex_label.setText(str(current_char.dexterity))
        self.con_label.setText(str(current_char.constitution))
        self.int_label.setText(str(current_char.intel))
        self.wis_label.setText(str(current_char.wisdom))
        self.charisma_label.setText(str(current_char.charisma))
        self.lore_edit.blockSignals(True)
        self.lore_edit.setPlainText(current_char.lore or "")
        self.lore_edit.blockSignals(False)
        self.notes_edit.blockSignals(True)
        self.notes_edit.setPlainText(current_char.notes or "")
        self.notes_edit.blockSignals(False)
        self.character_changed.emit(current_char)
 
    def _save_lore(self):
        global current_char
        if current_char is not None:
            current_char.lore = self.lore_edit.toPlainText()
 
    def _save_notes(self):
        global current_char
        if current_char is not None:
            current_char.notes = self.notes_edit.toPlainText()
    
    def apply_accent(self, color: QColor):
        self.setStyleSheet(f"""
            CharacterSheetView {{
                border: 2px solid {color.name()};
                border-radius: 4px;
            }}
        """)


        
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
        self.charisma_input = QLineEdit()
        self.lore_input = QTextEdit()
        self.lore_input.setPlaceholderText("Backstory / lore (optional)")
        self.lore_input.setFixedHeight(80)
        

        layout.addRow("Please enter your name:", self.name_input)
        layout.addRow("Please enter your class:", self.class_input)
        layout.addRow("Please enter your Race:", self.race_input)
        layout.addRow("Please enter your strength:", self.strength_input)
        layout.addRow("Please enter your dexterity:", self.dexterity_input)
        layout.addRow("Please enter your constitution:", self.constitution_input)
        layout.addRow("Please enter your intel:", self.intel_input)
        layout.addRow("Please enter your wisdom:", self.wisdom_input)
        layout.addRow("Please enter your charisma:", self.charisma_input)
        layout.addRow("Lore (optional):", self.lore_input)

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
            "wisdom":self.wisdom_input.text(),
            "charisma":self.charisma_input.text(),
            "lore": self.lore_input.toPlainText()}
    
    def accept(self):
        
        int_fields = {
            "Strength": self.strength_input,
            "Dexterity": self.dexterity_input,
            "Constitution": self.constitution_input,
            "Intelligence": self.intel_input,
            "Wisdom": self.wisdom_input,
            "charisma": self.charisma_input
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
    roll_completed = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.setStyleSheet(f"""
            DiceView {{
                border: 2px solid #4B1414;
                border-radius: 4px;
            }}
        """)

    
        self.dice = DiceWidget(self)

        self.dice_select = QComboBox(self)
        self.dice_select.addItems(["d4", "d6", "d8", "d10", "d12", "d20"])
        self.dice_select.setCurrentText("d20")
        self.dice_select.currentTextChanged.connect(
            lambda text: self.dice.set_dice(int(text[1:]))
        )
        self.dice.roll_completed.connect(self.roll_completed)

        panel_layout = QVBoxLayout(self)
        panel_layout.addWidget(self.dice)
        panel_layout.addWidget(self.dice_select)

    def diceroll(self):
        global die
        die = Dice(self.die_type)
        global roll
        roll = str(die.roll_dice("str"))
        self.button.setText(roll)

    def apply_accent(self, color: QColor):
        self.setStyleSheet(f"""
            DiceView {{
                border: 2px solid {color.name()};
                border-radius: 4px;
            }}
        """)

        

# Multiplier View
class MultiplierView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self._apply_style("#4B1414")

        outer = QVBoxLayout(self)

        title = QLabel("Modifiers")
        title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(title)

        # Header row
        grid = QGridLayout()
        grid.setColumnStretch(0, 3)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)

        for col, text in enumerate(["Stat", "Mod", "Roll"]):
            lbl = QLabel(text)
            lbl.setFont(QFont("Inter", 10, QFont.Weight.Bold))
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: #aaa; border-bottom: 1px solid #4B1414;")
            grid.addWidget(lbl, 0, col)

        stats = [
            ("Strength",     "str"),
            ("Dexterity",    "dex"),
            ("Constitution", "con"),
            ("Intelligence", "int"),
            ("Wisdom",       "wis"),
            ("Charisma",     "char"),
        ]

        self.result_labels = []
        self.mod_labels = []
        self._stat_keys = [key for _, key in stats]

        _d = Dice()
        self._current_mods = {key: _d.print_mod(key) for key in self._stat_keys}
 
        for row, (label_text, key) in enumerate(stats, start=1):
            name_lbl = QLabel(label_text)
 
            mod_val = self._current_mods[key]
            mod_sign = "+" if mod_val >= 0 else ""
            mod_lbl = QLabel(f"{mod_sign}{mod_val}")
            mod_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mod_lbl.setStyleSheet(f"color: #6dbf6d; font-weight: bold;")
            self.mod_labels.append((key, mod_lbl))
 
            result_lbl = QLabel("—")
            result_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            result_lbl.setFont(QFont("Inter", 12, QFont.Weight.Bold))
            result_lbl.setStyleSheet(f"color: #ffffff;")
            self.result_labels.append(result_lbl)
 
            grid.addWidget(name_lbl,   row, 0)
            grid.addWidget(mod_lbl,    row, 1)
            grid.addWidget(result_lbl, row, 2)
 
        
 
        outer.addLayout(grid)
        outer.addStretch()
 
    def update_mods(self, character):
        """Called when the active character changes. Recalculates all mods."""
        _d = Dice()
        if character is None:
            # Reset to zero mods when no character selected
            for key in self._stat_keys:
                self._current_mods[key] = 0
        else:
            stat_map = {
                "str":  character.strength,
                "dex":  character.dexterity,
                "con":  character.constitution,
                "int":  character.intel,
                "wis":  character.wisdom,
                "char": 0,  # not on Character yet; stays 0
            }
            for key, stat_val in stat_map.items():
                clamped = max(1, min(int(stat_val or 0), 20))
                result = _d.mod(clamped)
                self._current_mods[key] = result if result is not None else 0
        # Refresh mod labels
        for key, lbl in self.mod_labels:
            val = self._current_mods[key]
            sign = "+" if val >= 0 else ""
            lbl.setText(f"{sign}{val}")
 
        # Clear roll column since character changed
        for lbl in self.result_labels:
            lbl.setText("—")
 
    def on_roll_completed(self, raw: int):
        """Shows raw+mod for each stat in the Roll column, and the sum in Total."""
        running_total = 0
        for i, result_lbl in enumerate(self.result_labels):
            key = self._stat_keys[i]
            mod = self._current_mods[key]
            val = raw + mod
            running_total += val
            sign = "+" if mod >= 0 else ""
            result_lbl.setText(f"{val}")
        
 
    def _apply_style(self, color):
        self.setStyleSheet(f"""
            MultiplierView {{
                border: 2px solid {color};
                border-radius: 4px;
            }}
        """)
 
    def apply_accent(self, color: QColor):
        self._apply_style(color.name())

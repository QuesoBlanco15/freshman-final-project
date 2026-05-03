#creates characters that are used to display the current character
class Character:
    def __init__(self,is_set = False, name="",clas="",race="",strength=0,dexterity=0,constitution=0,intel=0,wisdom=0,charisma = 0,lore=""):
        self.is_set = is_set
        self.name = name
        self.clas = clas
        self.race = race
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intel = intel
        self.wisdom = wisdom
        self.charisma = charisma
        self.lore = lore

        @property
        def is_set(self):
            return self.is_set
        
        @is_set.setter
        def is_set(self,new_set):
            self.is_set = new_set
            
        @property
        def name(self):
            return self.name
        
        @name.setter
        def name(self,new_name):
            self.name = new_name

        @property
        def clas(self):
            return self.clas
        
        @clas.setter
        def clas(self,new_clas):
            self.clas = new_clas

        @property
        def race(self):
            return self.race
        
        @race.setter
        def race(self, new_race):
            self.race = new_race

        @property
        def strength(self):
            return self.strength
        
        @strength.setter
        def strength(self,new_strength):
            self.strength = new_strength

        @property
        def dexterity(self):
            return self.dexterity
        
        @dexterity.setter
        def dexterity(self,new_dexterity):
            self.dexterity = new_dexterity

        @property
        def constitution(self):
            return self.constitution
        
        @strength.setter
        def constitution(self,new_constitution):
            self.constitution = new_constitution

        @property
        def intel(self):
            return self.intel
        
        @intel.setter
        def intel(self,new_intel):
            self.intel = new_intel

        @property
        def wisdom(self):
            return self.wisdom
        
        @wisdom.setter
        def wisdom(self,new_wisdom):
            self.wisdom = new_wisdom

        @property
        def charisma(self):
            return self.charisma
        
        @charisma.setter
        def charisma(self,new_charisma):
            self.charisma = new_charisma

import Effects
import random
#print card content from cardset
def display_cards(cards):
    for card in cards: print("\t"+str(card))
#find card by card id in given card set
def find_card(id, card_set):
    for card in card_set:
        if card.id == id:
            return card
    return False
#select card from given card set through user input (through specifying card id)
def select(card_set, condition = lambda x : True):
    id = input("Enter id of the card to select (enter \"n/a\" to not select any): ")
    card = find_card(id, card_set)
    #keep asking until we get acceptable input
    while id != "n/a" and (not card or not condition(card)):
        print("invalid selection\n" if not card else "card not currently available\n")
        id = input("Enter id of the card to select (enter \"n/a\" to not select any): ")
        card = find_card(id, card_set)
    return None if id == "n/a" else card
#abstract class to represent a general card
class Card:
    def __init__(self, name, mana_cost, card_type, description, player):
        self.name = name
        self.mana_cost = mana_cost
        self.card_type=card_type
        self.description = description
        self.id = "Default"
        #pointer to actual battlefield (modifies the actual thing, not a copy)
        self.player = player
    def incur_effects(self):#activate all effects of card
        oppB = self.player.opp_battlefield
        myB = self.player.my_battlefield
        all_friendly = myB.hidden|myB.normal|myB.priori #all friendly cards
        all_enemy = oppB.hidden|oppB.normal|oppB.priori #all enemy cards
        for i in range(len(self.effects)):
            targets = []
            if self.targetting[i] == "SPECIFIC":#only for spells so far
                print("\nSELECT TARGET TO INCUR EFFECT ON")
                targets = [select(oppB.priori|oppB.normal|{self.player.opponent.me})] #stealth minions are immune to specific targetting (but not area or random effects)
                if targets == [None]: continue #no target is selected so we skip this iteration
            elif self.targetting[i] == "ENEMY": targets = list(all_enemy) #select all enemy minions
            elif self.targetting[i] == "ENEMY-R": targets = [list(all_enemy)[random.randint(0,len(all_enemy)-1)]] if len(all_enemy) > 0 else [] #select a random enemy minion
            elif self.targetting[i] == "FRIENDLY": targets = list(all_friendly) #select all friendly minions
            elif self.targetting[i] == "FRIENDLY-O": targets = list(all_friendly - {self.player.me}) #select all friendly minions except yourself
            elif self.targetting[i] == "SELF": targets = [self]
            self.effects[i](targets, self.scalars[i], self.player)
    def play(self, target):
        pass
    def copy(self):
        return Card(self.name, self.mana_cost, self.card_type, self.description, self.player)
    def __str__(self):
        return f"{self.id} - {self.name} (Mana Cost: {self.mana_cost}) - {self.description}"
#includes all people (hero and minions)
class Character(Card):
    def __init__(self, name, mana_cost, attack, health, description, player):
        super(Character, self).__init__(name, mana_cost, "character", description, player)
        self.attack = attack
        self.hp = health
        self.max_hp = health
    def __str__(self):
        return f"{self.id} - {self.name} (Mana Cost: {self.mana_cost}, Total Health: {self.max_hp}, Attack: {self.attack}) - {self.description}"
class Hero(Character):
    def __init__(self, name, health, description):
        super(Hero, self).__init__(name, 0, 0, health, description, None)
        self.card_type = "hero"
#Minion cards
class Minion(Character):
    def __init__(self, name, mana_cost, attack, health, description, combat_mode="N", effects=[], scalars=[], targetting=[], player=None):
        super(Minion,self).__init__(name, mana_cost, attack, health, description, player)
        self.card_type = "minion"
        self.active = (combat_mode == "C") #immediately active iff is "Charge"
        self.effects = effects
        self.scalars = scalars
        self.targetting = targetting
        self.combat_mode = combat_mode
    def play(self, target):
        target.hp -= self.attack
        self.hp -= target.attack
    def copy(self):#creates an unscathed identical minion
        return Minion(self.name, self.mana_cost, self.attack, self.max_hp, self.description, self.combat_mode, self.effects, self.scalars, self.targetting, self.player)
#Spell cards
class Spell(Card):
    def __init__(self, name, mana_cost, description, effects=[], scalars=[], targetting=[], player=None):
        super(Spell,self).__init__(name, mana_cost, "spell", description, player)
        self.effects = effects
        self.scalars = scalars
        self.targetting = targetting
        self.player = player
    def play(self): self.incur_effects()
    def copy(self):
        return Spell(self.name, self.mana_cost, self.description, self.effects, self.scalars, self.targetting, self.player)
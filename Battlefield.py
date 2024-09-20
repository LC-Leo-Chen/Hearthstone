#Battlefield: stores active minions, specific to each player
class Battlefield:
    #initialize battlefield
    def __init__(self):
        #O(1) add and remove with hash tables
        self.priori = set()
        self.hidden = set()
        self.normal = set()
    #add minion to set of minions on battlefield
    def add_minion(self, minion):
        if minion.combat_mode == "S": self.hidden.add(minion)
        elif minion.combat_mode == "T": self.priori.add(minion)
        else: self.normal.add(minion)
    #remove minions that are killed (cleanup)
    def remove_dead(self):
        #filter out dead minions, and point to the remaining ones as the set of minions
        #it is done this way because we cannot delete while iterating the set at the same time
        self.priori = set([minion for minion in self.priori.copy() if minion.hp > 0])
        self.normal = set([minion for minion in self.normal.copy() if minion.hp > 0])
        self.hidden = set([minion for minion in self.hidden.copy() if minion.hp > 0])
    def re_activate(self):
        for minion in self.priori|self.normal|self.hidden: minion.active = True
    def make_visible(self, minion):
        if minion.combat_mode == "S":
            self.hidden.remove(minion)
            self.normal.add(minion)
    def display_battlefield(self):
        info = lambda minion:\
                f"\t{minion.id} - {minion.name} (hp: {minion.hp}/{minion.max_hp}, atk: {minion.attack}, { str('' if minion.active else 'IN') }ACTIVE)"
        print("TAUNT (would have to be hit first):")
        if len(self.priori) > 0:
            for minion in self.priori: print(info(minion))
        else: print("\t(None)")
        print("STEALTH (cannot be specifically targetted):")
        if len(self.hidden) > 0 :
            for minion in self.hidden: print(info(minion))
        else: print("\t(None)")
        print("NORMAL:")
        if len(self.normal) > 0:
            for minion in self.normal: print(info(minion))
        else: print("\t(None)")
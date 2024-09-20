import random
import Cards
class Player:
    #initialize player
    def __init__(self, deck, my_battlefield, me):
        self.me = me
        self.my_battlefield = my_battlefield
        self.opponent = None
        self.opp_battlefield = None
        me.player = self
        random.shuffle(deck)
        self.deck = deck
        self.hand = set()
        self.mana_crystals = 1
        #to distinguish between different cards with ID
        self.id = 1
    #draw a card from card deck
    def draw_card(self):
        #draw from top of the deck
        if len(self.deck) > 0:
            card = self.deck.pop(0)
            #make it distinct from one another to prevent same-card collision in set
            copy = card.copy()
            copy.player = self
            #assign unique id to card
            copy.id = str(self.id)
            self.id += 1
            #display this new card
            self.hand.add(copy)
            print("NEW CARD: "+str(card))
            return True
        return False
    #draw initial hand (at the beginning of the game)
    def draw_starting_hand(self, card_count):
        print(f"{self.me.name}'s starting hand:")
        for _ in range(card_count):
            if not self.draw_card():
                return False
        return True
    #print player status
    def display_stats(self):
        print("-" * 100)
        print("STATUS:\n")
        print(f"Your Hero: {self.me.name} (hp: {self.me.hp}/{self.me.max_hp}, id: {self.me.id})")
        print("Your Deployed Minions:\n")
        self.my_battlefield.display_battlefield()
        print(f"\nOpponent's Hero: {self.opponent.me.name} (hp: {self.opponent.me.hp}/{self.opponent.me.max_hp}, id: {self.opponent.me.id})")
        print("Opponent's Deployed Minions:\n")
        self.opp_battlefield.display_battlefield()
        print("\nYour Current Hand:")
        for card in self.hand: print(f"\t{card}")
        print(f"Mana Crystals: {self.mana_crystals}\n")
    def take_turn(self):
        current_mana = self.mana_crystals
        myB = self.my_battlefield
        oppB = self.opp_battlefield
        #cast spells or deploy new minions)
        while True:
            self.display_stats()
            #select card
            card = Cards.select(self.hand, lambda x : x.mana_cost <= self.mana_crystals)
            if card == None: break #exit card selection process if none are to be selected
            #deploy card
            self.mana_crystals -= card.mana_cost
            self.hand.remove(card)
            #process card (add minion to battlefield and cast spells)
            if card.card_type == "minion":#add minion to battle field
                card.incur_effects()
                myB.add_minion(card)
            elif card.card_type == "spell":#cast spell onto a target
                card.play()
                if self.opponent.me.hp <= 0: return True #end game if opponent is killed
            else: pass#can be extended in the future
            #clean up dead minions on both sides
            myB.remove_dead()
            oppB.remove_dead()
        #command minions
        while True:
            #select a active minion to attack from and a target minion to be attacked
            self.display_stats()
            print("SELECT ACTIVE DEPLOYED MINION")
            my_minion = Cards.select(myB.priori|myB.normal|myB.hidden, lambda x : x.active)
            if my_minion == None: break #this means we quit because no minions are chosen
            print("\nSELECT OPPONENT TARGET TO HIT")
            #must attack taunt minions before attacking normal minions. Minions in stealth are immune to attack
            target_set = oppB.priori if len(oppB.priori) > 0 else oppB.normal
            opp_minion = Cards.select(target_set | {self.opponent.me}) #allow heroes to be hit
            if opp_minion == None: continue #this means we cancel targetting for this minion, but we don't quit
            #initiate attack
            my_minion.play(opp_minion)
            my_minion.active = False #deactivate minion after use
            myB.make_visible(my_minion) #move minion out of stealth (no effect if originally not in stealth)
            #check if opponent is killed (opponent only reacts so it is impossible for attacker to be killed)
            if self.opponent.me.hp <= 0: return True
            #cleanup dead minions on both sides
            myB.remove_dead()
            oppB.remove_dead()
        myB.re_activate() #set cards in hand to become active
        self.mana_crystals = current_mana #regain the manna level
        return False
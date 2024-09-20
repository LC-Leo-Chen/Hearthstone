import random
import Effects
from Cards import Hero, display_cards
from Battlefield import Battlefield
from Player import Player
from Card_Definitions import minions, spells

def main():
    #display cards
    print("Minions of the card deck:")
    display_cards(minions)
    print("Spells of the card deck:")
    display_cards(spells)
    #create card decks
    card_set = minions + spells
    deck = [card_set[random.randint(0,len(card_set)-1)] for i in range(30)]
    #get player names
    player1_name=input("Enter Player 1 name: ")
    player2_name=input("Enter Player 2 name: ")
    #initialize battlefield for both players
    player1_Bfield=Battlefield()
    player2_Bfield=Battlefield()
    #initialize heroes for both players
    p1_card = Hero(player1_name, 30, "hero")
    p1_card.id = '0'
    p2_card = Hero(player2_name, 30, "hero")
    p2_card.id = '0'
    #initialize both players
    print("-" * 100)
    player1 = Player(deck.copy(), player1_Bfield, p1_card)
    player2 = Player(deck.copy(), player2_Bfield, p2_card)
    player1.opponent = player2
    player1.opp_battlefield = player2_Bfield
    player2.opponent = player1
    player2.opp_battlefield = player1_Bfield
    #start game
    player1.draw_starting_hand(3)
    player2.draw_starting_hand(4) #player who goes second gets an extra draw at the beginning
    print("-" * 100)
    players = [player1, player2]
    turn = 0 #to specify whose turn this round is
    while True:
        #draw new cards at the beginning of each new round
        print(f"It is now {players[turn].me.name}'s turn")
        if not players[turn].draw_card():
            print("Deck is empty, no card is drawn")
        #process player actions for the player's turn
        game_ends = players[turn].take_turn()
        if game_ends:
            print("\n\n")
            print(f"{players[turn].me.name} WINS THE MATCH!!!")
            break
        #update player mana
        players[turn].mana_crystals = min(10, players[turn].mana_crystals + 1)
        turn^=1 #switch to the other player
        print("-" * 100)
main()
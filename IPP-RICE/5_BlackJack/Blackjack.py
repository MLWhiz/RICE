# Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K') 
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        print_str = ""
        for card in self.cards:
            print_str+= str(card)+" "
        return "Hand Contains: " + print_str

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0 
        for card in self.cards:
            rank = card.get_rank()
            value += VALUES[rank]
        if 'A' in [card.get_rank() for card in self.cards]:
            if value+10<=21:
                value +=10
        return value

    def draw(self, canvas, pos):
        i = 0
        for card in self.cards:
            pos[0]=pos[0]+80

            card.draw(canvas, pos)
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for rank in RANKS:
            for suit in SUITS:
                card = Card(suit,rank)
                self.cards.append(card)

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def __str__(self):
        print_str = ""
        for card in self.cards:
            print_str+= str(card)+" "
        return "Deck Contains: " + print_str



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand,score
    if in_play:
        score -= 1
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    print "Player:" + str(player_hand)
    print "Dealer:" + str(dealer_hand)
    in_play = True
    outcome = ""

def hit():
    global player_hand,outcome,in_play,deck,score
    if in_play:
        player_hand.add_card(deck.deal_card())
        print "Player:" + str(player_hand)
        hand_value = player_hand.get_value()
        if hand_value>21:
            outcome = "You have busted"
            in_play = False
            score-=1
        print outcome

    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global dealer_hand,deck,outcome,in_play,score
    if in_play:
        while dealer_hand.get_value()<17:
            dealer_hand.add_card(deck.deal_card())
        print "Dealer:" + str(dealer_hand)
        dealer_hand_val = dealer_hand.get_value()
        if dealer_hand_val>21:
            outcome = "Dealer has busted. You win"
            score+=1
            in_play = False
        elif dealer_hand_val >= player_hand.get_value():
            outcome = "Dealer Wins"
            score-=1
            in_play = False
        else:
            outcome = "You Win"
            score+=1
            in_play = False
        print outcome
    else:
        print outcome
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# define global program values

deck = Deck()
player_hand = Hand()
dealer_hand = Hand()

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome,score
    canvas.draw_text('Blackjack',[250,30],26 , "White")
    canvas.draw_text('Player Hand',[50,80],18 , "Blue")
    canvas.draw_text('Player Score: ' + str(player_hand.get_value()) ,[250,80],18 , "Black")
    player_hand.draw(canvas,[50,100])
    canvas.draw_text('Dealer Hand',[50,280],18 , "Blue")
    canvas.draw_text('dealer Score: ' + str(dealer_hand.get_value()) ,[250,280],18 , "Black")
    dealer_hand.draw(canvas,[50,300])
    canvas.draw_text(outcome,[250,500],26 , "Red")
    if outcome == "":
        canvas.draw_text("Hit or Stand?",[250,500],26 , "Red")
    if not in_play:
        canvas.draw_text("New Deal?",[250,550],26 , "Red")
    if in_play:
        card_loc = (CARD_CENTER[0] , CARD_CENTER[1] )
        canvas.draw_image(card_back, card_loc, CARD_SIZE, [50+80 + CARD_CENTER[0], 300 + CARD_CENTER[1]], CARD_SIZE)
    canvas.draw_text('Games Won: ' + str(score) ,[400,80],18 , "Black")
        



# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
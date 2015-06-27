# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random

SECRET_NUM = 50
GUESSES_ALLOWED = 7
CURRENT_RANGE = 0

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global SECRET_NUM,GUESSES_ALLOWED
    SECRET_NUM = random.randrange(0,100)
    GUESSES_ALLOWED = 7
    
    

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global CURRENT_RANGE
    CURRENT_RANGE=0
    print "Starting a New Game with Range [0,100). You have 7 Guesses"
    new_game()   

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global CURRENT_RANGE
    CURRENT_RANGE=1
    new_game()
    global SECRET_NUM,GUESSES_ALLOWED
    SECRET_NUM = random.randrange(0,1000)
    GUESSES_ALLOWED = 10
    print "Starting a New Game with Range [0,1000). You have 10 Guesses"

    
def input_guess(guess):
    # main game logic goes here	
    global GUESSES_ALLOWED,CURRENT_RANGE
    GUESSES_ALLOWED-=1
    guess = int(guess)
    print "Guess Was "+str(guess)
    if guess == SECRET_NUM:
        print "Guesses_remaining "+str(GUESSES_ALLOWED)
        print "Correct"
    elif guess < SECRET_NUM:
        print "Guesses_remaining "+str(GUESSES_ALLOWED)
        print "Higher"
    else:
        print "Guesses_remaining "+str(GUESSES_ALLOWED)
        print "Lower"
    if GUESSES_ALLOWED==0 and guess != SECRET_NUM:
        print "You Lose"
        if CURRENT_RANGE==0:
            range100()
        else:
            range1000()
    
# create frame
frame = simplegui.create_frame('Guess The Number', 200, 200)
guess = frame.add_input('Input your Guess', input_guess, 100)
btn1 = frame.add_button('Range:0-100', range100, 100)
btn2 = frame.add_button('Range:0-1000', range1000, 100)
# register event handlers for control elements and start frame


# call new_game 
new_game()


# always remember to check your completed program against the grading rubric

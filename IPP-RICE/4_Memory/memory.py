# implementation of card game - Memory

import simplegui
import random

deck = []
exposed = []
state = 0
ultimate = 0
penultimate = 0 
counter = 0 
# helper function to initialize globals
def new_game():
    global deck,exposed
    deck = [x for x in range(0,8)]*2
    random.shuffle(deck)
    exposed = [False for x in range(16)]
    global state,counter
    state = 0
    counter = 0
    
     
# define event handlers
def mouseclick(pos):
    # add game state logic here

    global state,exposed,ultimate,penultimate,counter
    click_index = pos[0]/50
    if exposed[click_index]:
        pass
    else:
        exposed[click_index] = True
        if state == 0:
            state = 1
        elif state == 1:
            state = 2
            counter+=1
        else:
            if deck[ultimate]!=deck[penultimate]:
                exposed[ultimate]=False
                exposed[penultimate]=False
            state = 1
            counter+=1
        penultimate,ultimate = ultimate,click_index    

               
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(len(deck)):
        if exposed[i]:
            canvas.draw_text(str(deck[i]), [20+50*i,60],32, 'Red')
        else:
            canvas.draw_polygon([(50*i, 0), (50*(i+1), 0), (50*(i+1), 100),(50*i,100)], 1, 'Green','Red')
    label.set_text('Turns = '+str(counter))


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
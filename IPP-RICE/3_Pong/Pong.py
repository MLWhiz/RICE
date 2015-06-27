# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2,HEIGHT/2]
    if direction:
        ball_vel = [3,-3]
    else:
        ball_vel = [-3,-3]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2 
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)

def reset_handler():
    new_game()


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel,RIGHT,LEFT
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    
    # draw ball
    canvas.draw_circle((ball_pos[0], ball_pos[1]), BALL_RADIUS, 1, 'Green','Green')
    # update paddle's vertical position, keep paddle on the screen
    if 0<paddle1_pos+paddle1_vel+PAD_HEIGHT/2<HEIGHT and 0<paddle1_pos+paddle1_vel-PAD_HEIGHT/2<HEIGHT:
        paddle1_pos+=paddle1_vel
    if 0<paddle2_pos+paddle2_vel+PAD_HEIGHT/2<HEIGHT and 0<paddle2_pos+paddle2_vel-PAD_HEIGHT/2<HEIGHT:
        paddle2_pos+=paddle2_vel
    # draw paddles
    #Left Paddle
    canvas.draw_polygon([[0,paddle1_pos-PAD_HEIGHT/2], [0,paddle1_pos+PAD_HEIGHT/2], [PAD_WIDTH,paddle1_pos+PAD_HEIGHT/2], [PAD_WIDTH, paddle1_pos-PAD_HEIGHT/2]], 12, 'Yellow', 'Orange')
    #Right Paddle
    canvas.draw_polygon([[WIDTH-PAD_WIDTH,paddle2_pos-PAD_HEIGHT/2], [WIDTH-PAD_WIDTH,paddle2_pos+PAD_HEIGHT/2], [WIDTH,paddle2_pos+PAD_HEIGHT/2], [WIDTH, paddle2_pos-PAD_HEIGHT/2]], 12, 'Yellow', 'Orange')
    
    #determine if top collides or bottom collides
    if  0>=ball_pos[1]-BALL_RADIUS or ball_pos[1]+BALL_RADIUS>=HEIGHT - 1:
        ball_vel[1]*=-1

    #determine whether paddle and ball collide    
    
    if  paddle1_pos-PAD_HEIGHT/2  <=ball_pos[1] <= paddle1_pos+PAD_HEIGHT/2 and ball_pos[0]-BALL_RADIUS<=PAD_WIDTH:
        # Ball collides with the left paddle
        ball_vel[0] *= -1.1
    elif paddle2_pos-PAD_HEIGHT/2  <=ball_pos[1] <= paddle2_pos+PAD_HEIGHT/2 and ball_pos[0]+BALL_RADIUS>=WIDTH-1-PAD_WIDTH:
        # Ball collides with the left paddle
        ball_vel[0] *= -1.1
    elif ball_pos[0]+BALL_RADIUS>=WIDTH-1-PAD_WIDTH:
        score1+=1
        spawn_ball(LEFT)
    elif ball_pos[0]-BALL_RADIUS<=PAD_WIDTH:
        score2+=1
        spawn_ball(RIGHT)
    # draw scores
    canvas.draw_text(str(score1), (WIDTH/4, HEIGHT/2), 35, 'Red')
    canvas.draw_text(str(score2), (3*WIDTH/4, HEIGHT/2), 35, 'Red')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = -3
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = acc
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel = -acc
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel = acc
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel = -acc
   

   
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel=0
    paddle2_vel=0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
button2 = frame.add_button('Restart', reset_handler, 70)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()

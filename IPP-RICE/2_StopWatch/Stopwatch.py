# template for "Stopwatch: The Game"
import simplegui

# define global variables
time_ctr = 0
success = 0
attempts = 0 

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    # 12 means 1.2 sec
    seconds_past = t/10.0
    mins = int(seconds_past/60)
    seconds = str(seconds_past % 60)
    if len(seconds.split(".")[0])!=2:
        seconds="0"+seconds
    return str(mins)+":"+seconds


# define event handlers for buttons; "Start", "Stop", "Reset"
def button_handler_start():
    timer.start()
    
def button_handler_stop():
    global attempts, success
    if timer.is_running():
        attempts += 1
        if time_ctr % 10==0:
            success += 1
    timer.stop()
    
def button_handler_reset():
    global time_ctr,attempts, success
    timer.stop()
    time_ctr = 0
    attempts = 0
    success = 0


# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time_ctr
    time_ctr+=1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(time_ctr),[100,100], 24, "White")
    if attempts>=1:
        canvas.draw_text(str(float(success)/float(attempts)),[280,10], 12, "White")
# create frame
frame = simplegui.create_frame('Testing', 300, 300)

# register event handlers
buttonstart = frame.add_button('Start', button_handler_start, 50)
buttonstop = frame.add_button('Stop', button_handler_stop, 50)
buttonreset = frame.add_button('reset', button_handler_reset, 50)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, timer_handler)

# start frame
frame.start()

# Please remember to review the grading rubric

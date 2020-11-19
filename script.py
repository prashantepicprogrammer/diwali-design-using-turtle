from turtle import Screen, Turtle
import colorsys
import random
import math

COLOR = (0.60156, 0, 0.99218)  
TARGET = (0.86328, 0.47656, 0.31250) 

screen = Screen()
screen.tracer(False)

WIDTH, HEIGHT = screen.window_width(), screen.window_height()

deltas = [(hue - COLOR[index]) / HEIGHT for index, hue in enumerate(TARGET)]

turtle = Turtle()
turtle.color(COLOR)

turtle.penup()
turtle.goto(-WIDTH/2, HEIGHT/2)
turtle.pendown()

direction = 1

for distance, y in enumerate(range(HEIGHT//2, -HEIGHT//2, -1)):

    turtle.forward(WIDTH * direction)
    turtle.color([COLOR[i] + delta * distance for i, delta in enumerate(deltas)])
    turtle.sety(y)

    direction *= -1

turtle.penup()
turtle.home()
turtle.backward(200)
turtle.right(90)
turtle.pendown()


turtle.write("Happy Diwali", font=("Verdana", 50, "normal"))

H_PINK = 0.90  
V_DARK = 0.40  
V_BRIGHT = 1  
FPS = 30  
TIMER_VALUE = 1000//FPS  
CYCLE = 5  
LIGHTUP_TIME = 1  
SPEED = 20 #  
CLOSE_ENOUGH = 16  
N = 300  

PHASE_DELTA = 0.01 

fireflies = []  
v = []  
phase = []  
current_xpos = []  
current_ypos = []  
target_xpos = [] 
target_ypos = []  

def initialze_fireflies():
    for i in range(N):
        fireflies.append(Turtle()) 
        v.append(V_DARK) 
        phase.append(random.uniform(0,CYCLE))  
        current_xpos.append(random.uniform(-500,500))  
        current_ypos.append(random.uniform(-500,500))
        target_xpos.append(random.uniform(-500,500))
        target_ypos.append(random.uniform(-500,500))

    for firefly in fireflies:  
        firefly.hideturtle()
        firefly.up()


def compute_brightness(phase):
    if phase < CYCLE-LIGHTUP_TIME:
        temp = V_DARK  
    elif phase < CYCLE-LIGHTUP_TIME/2:  
        temp = V_DARK + (V_BRIGHT-V_DARK)*(phase-(CYCLE-LIGHTUP_TIME))/(LIGHTUP_TIME/2)
    else: 
        temp = V_BRIGHT - (V_BRIGHT-V_DARK)*(phase-(CYCLE-LIGHTUP_TIME/2))/(LIGHTUP_TIME/2)
    return temp

def update_neibors(k):
    global phase
    for i in range(N):
        if i == k or phase[i] == CYCLE-LIGHTUP_TIME/2:  
            continue
        if phase[i] < CYCLE-LIGHTUP_TIME/2:  
            phase[i] = min(CYCLE-LIGHTUP_TIME/2,phase[i]+PHASE_DELTA)  
        else:  
            phase[i] += PHASE_DELTA  
            if phase[i] > CYCLE:  
                phase[i] -= CYCLE  
        v[i] = compute_brightness(phase[i])  
                
def update_brightness():
    global phase,v
    for i in range(N):
        phase[i] += TIMER_VALUE/1000  
        if phase[i] > CYCLE:  
            phase[i] -= CYCLE  
        if phase[i] > CYCLE-LIGHTUP_TIME/2 and phase[i] - TIMER_VALUE/1000 < CYCLE-LIGHTUP_TIME/2: # skipped peak
            phase[i] = CYCLE-LIGHTUP_TIME/2  
        v[i] = compute_brightness(phase[i]) 

    for i in range(N): 
       if phase[i] == CYCLE-LIGHTUP_TIME/2: 
            update_neibors(i) 

def update_position():
    global current_xpos,current_ypos,target_xpos,target_ypos
    for i in range(N):
        
        angle_to_target = math.atan2(target_ypos[i]-current_ypos[i],target_xpos[i]-current_xpos[i])
         
        current_xpos[i] += SPEED/FPS*math.cos(angle_to_target)
        current_ypos[i] += SPEED/FPS*math.sin(angle_to_target)
         
        dist_to_target_squared = (current_xpos[i]-target_xpos[i])**2 + (current_ypos[i]-target_ypos[i])**2
        if dist_to_target_squared < CLOSE_ENOUGH: 
            target_xpos[i] = random.randint(-500,500)  
            target_ypos[i] = random.randint(-500,500)  
        
def update_states():
    global should_draw
    update_brightness()
    update_position()
    should_draw = True
    screen.ontimer(update_states,TIMER_VALUE)

def draw():
    global v,fireflies,should_draw,current_xpos,current_ypos
    if should_draw == False:  
        return
    for i in range(N):
        fireflies[i].clear() 
        color = colorsys.hsv_to_rgb(H_PINK,1,v[i])  
        fireflies[i].color(color)
        fireflies[i].goto(current_xpos[i],current_ypos[i])
        fireflies[i].dot(10)
    should_draw = False  

# screen.bgcolor('black')
initialze_fireflies()                
update_states()
while True:
    draw() # draw forever
    screen.update()
turtle.forward(100)

#test up


# side stick
# turtle.color('#770D07')
# turtle.begin_fill()
# turtle.forward(250)
# turtle.left(90)
# turtle.forward(5)
# turtle.left(90)
# turtle.forward(250)
# turtle.end_fill()

# # upper triangle
# turtle.begin_fill()
# turtle.right(45)
# turtle.forward(50)
# turtle.right(90)
# turtle.forward(50)
# turtle.left(90)
# turtle.forward(5)
# turtle.left(90)
# turtle.forward(50+5)
# turtle.left(90)
# turtle.forward(50+5+2+2)
# turtle.end_fill()

# # triangle end
# turtle.begin_fill()
# turtle.right(-30-90-15)
# turtle.forward(80)
# turtle.right(90)
# turtle.forward(5)
# turtle.right(90)
# turtle.forward(80)
# turtle.end_fill()



screen.tracer(True)
screen.exitonclick()

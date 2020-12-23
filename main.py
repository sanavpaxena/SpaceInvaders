import turtle
import winsound
import math
import random
import platform
import os
from pygame import mixer

if platform.system() == "Windows":
    try:
        import winsound
    except:
        print("Winsound module not available.")

running = True

wn = turtle.Screen()
wn.screensize()
wn.setup(width=1.0, height=1.0)
wn.bgcolor('black')
wn.title('Space Invaders')
wn.bgpic("space_invaders_background.gif")
wn.tracer(0)

wn.register_shape("invader.gif")
wn.register_shape("player.gif")

is_pause = False

#BORDER
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color('white')
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color('white')
score_pen.penup()
score_pen.setposition(-290,300)
scorestring = "Score: %s"%score
score_pen.write(scorestring,False,align ="left",font = ("Arial",14,"normal"))
score_pen.hideturtle()

#PLAYER
player = turtle.Turtle()
player.shape('player.gif')
player.color('blue')
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)
playerspeed = 3

#ENEMY

num_enemies = 30
enemies = []

for i in range(num_enemies):
    enemies.append(turtle.Turtle())

enemy_start_x = -225
enemy_start_y = 250
enemy_number = 0


for enemy in enemies:
    enemy.shape('invader.gif')
    enemy.color('red')
    enemy.penup()
    enemy.speed(0)
    x = enemy_start_x + (50* enemy_number)
    y = enemy_start_y 
    enemy.setposition(x,y)

    enemy_number += 1
    if enemy_number == 10:
        
        enemy_start_y -= 50
        enemy_number = 0

enemyspeed = 0.1



bullet = turtle.Turtle()
bullet.color('yellow')
bullet.shape('triangle')
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle()

bulletspeed = 3

bulletstate = "ready"

def start_game():
    global game_state
    game_state = "game"


def toggle_pause():
    global is_pause
    if is_pause == True:
        is_pause = False
    else:
        is_pause = True

# def move_enemy():
#     x = enemy.xcor()
#     y = enemy.ycor()

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)

def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = -280
    player.setx(x)

def fire_bullet():
    global bulletstate
    if bulletstate == "ready":
        play_sound('laser.wav')
           
        bulletstate = "fire"
        x = player.xcor()
        y= player.ycor() + 10
        bullet.setposition(x,y)
        bullet.showturtle()

def Collision(t1,t2):
    distance  = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 15:
        return True
    else:
        return False

def play_sound(sound_file,time = 0):
    if platform.system() == "Windows":
        winsound.PlaySound(sound_file, winsound.SND_ASYNC)

    elif platform.system() == "Linux":
        os.system('aplay -q {}&'.format(sound_file))

    else:
        os.system("afplay {}&".format(sound_file))

    if time>0:
        wn.ontimer(lambda: play_sound(sound_file,time), t = int(time*1000))

def quit():
    global running
    running = False






wn.listen()
wn.onkeypress(move_right,"Right")
wn.onkeypress(move_left,"Left")
wn.onkeypress(toggle_pause,"p")
wn.onkeypress(fire_bullet,'space')
wn.onkeypress(start_game,"s") 
wn.onkeypress(quit, "q")



mixer.init()
mixer.music.load("bgm.wav")
mixer.music.play()

play_sound('bgm.wav', 119)

game_state = "splash"

while True:
    if not is_pause:
        for enemy in enemies:
            x = enemy.xcor()
            x += enemyspeed
            enemy.setx(x)

            if enemy.xcor() > 280:
                for e in enemies:
                        y = e.ycor()
                        y -= 40
                        e.sety(y)
                enemyspeed *= -1
                    
            if enemy.xcor() < -280:
                for e in enemies:
                    y = e.ycor()
                    y -= 40
                    e.sety(y)
                enemyspeed *= -1

            if Collision(bullet,enemy):
                bullet.hideturtle()
                bulletstate = "ready"
                bullet.setposition(0,-400)
                enemy.setposition(0,10000)


                play_sound("explosion.wav")
                score += 10
                scorestring = "Score: %s"%score
                score_pen.clear()
                score_pen.write(scorestring,False,align ="left",font = ("Arial",14,"normal"))


            if Collision(player,enemy):
                player.hideturtle()
                enemy.hideturtle()
            
                print("GAME OVER")
                break

        #### BULLET #####
        if bulletstate=="fire":
            y = bullet.ycor()
            y+= bulletspeed
            bullet.sety(y)
        if bullet.ycor() > 275:
            bullet.hideturtle()
            bulletstate = "ready"

        wn.update()

    else:
        wn.update()



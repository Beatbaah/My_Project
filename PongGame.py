import turtle
import os

wn = turtle.Screen()
wn.title('Pong Game')
wn.bgpic("halo.gif")
wn.setup(width = 800, height = 600)
wn.tracer(0)

#Score
score_a = 0
score_b = 0

#Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("DarkOrange3")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350,0)

#Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("DarkOrange3")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350,0)

#Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0,0)
ball.dx = 2
ball.dy = -2

#Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color('white')
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write("PlayerA: 0  PlayerB: 0", align = 'center', font=("Courier", 24, "bold"))

#Function
def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)

    
#Buildings
wn.listen()
wn.onkeypress(paddle_a_up, 'a') 
wn.onkeypress(paddle_a_down,'s')
wn.onkeypress(paddle_b_up, 'k') 
wn.onkeypress(paddle_b_down,'l')   

#main Game loop

while True:
    wn.update()

    #Moving the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    #Border Checks
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
        os.system("afplay sfx-boing3.mp3&")

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
        os.system("afplay sfx-boing3.mp3&")


    if ball.xcor() > 390:
        ball.goto(0,0)
        ball.dx *= -1
        score_a +=1
        pen.clear()
        pen.write("PlayerA: {} PlayerB: {}".format(score_a, score_b), align = 'center', font=("Courier", 24, "normal"))


    if ball.xcor() < -390:
        ball.goto(0,0)
        ball.dx *= -1 
        score_b +=1
        pen.clear()
        pen.write("PlayerA: {} PlayerB: {}".format(score_a, score_b), align = 'center', font=("Courier", 24, "normal"))

    
    #Paddle and ball collision
    if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() - 40):
        ball.setx(340)
        ball.dx *= -1
        os.system("afplay mixkit-soccer-ball-quick-kick-2108.wav&") 
 

    if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() - 40):
        ball.setx(-340)
        ball.dx *= -1
        os.system("afplay mixkit-soccer-ball-quick-kick-2108.wav&") 
    
    #increasing speed by 7
    #Increasing speed of the ball
    if (ball.dy > 0 and ball.dy < 5):
        ball.dy += 0.5
    elif(ball.dy < 0 and ball.dy > -5):
        ball.dy -= 0.5

    if (ball.dx > 0 and ball.dx < 5):
        ball.dx += 0.5
    elif(ball.dx < 0 and ball.dx > -5):
        ball.dx -= 0.5


    if (ball.dy > 0 and ball.dy < 7):
        ball.dy += 1
    elif(ball.dy < 0 and ball.dy > -7):
        ball.dy -= 1

    if (ball.dx > 0 and ball.dx < 7):
        ball.dx += 1
    elif(ball.dx < 0 and ball.dx > -7):
        ball.dx -= 1
    

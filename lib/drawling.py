import turtle, sys
from time import sleep

pen = turtle.Turtle()
turtle.title('Aguarde...')
turtle.bgcolor('black')

def ddd():
    def curve(): 
        for _ in range(200): 
            pen.right(1) 
            pen.forward(1) 

    def heart(): 
        pen.fillcolor('red') 
        pen.begin_fill() 
        pen.left(140) 
        pen.forward(113) 
        curve() 
        pen.left(120) 
        curve() 
        pen.forward(112) 
        pen.end_fill() 
        
    def txt(): 
        pen.up() 
        pen.setpos(-68, 95) 
        pen.down() 
        pen.color('lightgreen') 
        pen.write("I Love You", font=( 
        "Consolas", 17, "bold"))
        sleep(5)
    heart() 
    txt()


import turtle



class ShuffleGame:
    
    def __init__(self) -> None:
        
        self.win = turtle.Screen()
        self.win.title("Limbo")
        self.win.bgcolor("white")
        self.win.setup(width=800, height=800)
        self.win.tracer(0)
        
        self.turtle = turtle.Turtle()
        self.turtle.color('red')
        self.turtle.speed(0)
        self.turtle.hideturtle()
        
        self.keyPositions: dict = dict()
        
        
    def goto(self, _x: int, _y: int) -> None:
        
        self.turtle.penup()
        self.turtle.goto(_x, _y)
        self.turtle.pendown()
        
    def draw_key(self, _x, _y, color) -> None:
        
        self.goto(_x, _y)
        self.turtle.begin_fill()
        self.turtle.fillcolor(color)
        self.turtle.circle(50)
        self.turtle.end_fill()
        
    def start(self) -> None:
        
        self.draw_key(200, 200, 'red')
        
        while True:
            self.win.update()
        
        
        
if __name__ == '__main__':
    
    instance = ShuffleGame()
    instance.start()
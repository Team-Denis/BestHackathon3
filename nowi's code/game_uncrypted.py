
import turtle
import time
import random


class SwapTask:
    
    def __init__(self, id1, id2, x1, x2, y1, y2, dx, dy, steps: int = 100) -> None:
        
        self.ID1 = id1; self.ID2 = id2
        self.x1 = x1; self.x2 = x2; self.y1 = y1; self.y2 = y2
        self._dx = dx; self._dy = dy
        
        self.steps = steps
        self.current_step = 0
    
    def advanceStep(self) -> tuple[dict]:
        
        if not self.isDone():
            self.current_step += 1
            return {'target': self.ID1,'ft': self.current_step,
                    'new_x': self.x1 + self._dx*self.current_step,'new_y': self.y1 + self._dy*self.current_step}
                    
    def isDone(self) -> bool:
        return self.steps == self.current_step

class ShuffleGame:
    
    lookup_dict: dict = {
        (50, 200): 1,
        (175, 200): 2,
        (300, 200): 3,
        (425, 200): 4,
        (550, 200): 5,
        (50, 400): 6,
        (175, 400): 7,
        (300, 400): 8,
        (425, 400): 9,
        (550, 400): 10
    }
    
    def __init__(self) -> None:
        
        self.width = 600
        self.height = 600
        
        self.win = turtle.Screen()
        self.win.title("Limbo")
        self.win.bgcolor("gray")
        self.win.setup(width=self.width, height=self.height)
        self.win.tracer(0)
        
        self.turtle = turtle.Turtle()
        self.turtle.speed('fastest')
        self.turtle.hideturtle()
        
        self.infoTurtle = turtle.Turtle()
        self.infoTurtle.hideturtle()
        self.goto(self.infoTurtle, 35, 100)
        self.infoTurtle.write("Tentez de faire une streak de 3 ! (Actuelle : 0)", font=("Arial", 20, "normal"))
        
        self.keyPositions: dict[int: dict] = dict()
        self.taskPriorityQueue: list[list[SwapTask]] = []
        self.initKeys()
        
        self.swapNO = 0
        self.streak = 0
        self.speed = (300, 200, 50)
        self.swapsPerStreak = (6, 10, 30)
        self.freeze = True
        self.doneshuffling = False
        
    def goto(self, target_turtle, _x: int, _y: int) -> None:
        
        target_turtle.penup()
        target_turtle.goto(-self.width/2 + _x, self.height/2 - _y)
        target_turtle.pendown()
        
    def draw_key(self, _x, _y, color) -> None:
        
        self.goto(self.turtle, _x, _y)
        self.turtle.begin_fill()
        self.turtle.color(color)
        self.turtle.fillcolor(color)
        self.turtle.circle(20)
        self.turtle.end_fill()
    
    def updateKeys(self) -> None:
        
        self.turtle.clear()
        
        if self.taskPriorityQueue and not self.freeze:
            if self.taskPriorityQueue[0]:
                for task in self.taskPriorityQueue[0]:
            
                    p = task.advanceStep()
                    self.move(p['target'], p['new_x'], p['new_y'])
                    if task.isDone():self.taskPriorityQueue[0].remove(task)
                    
            else:
                self.taskPriorityQueue.pop(0)
                
        else:
            
            if self.swapNO != self.swapsPerStreak[self.streak] and not self.freeze:
                self.taskPriorityQueue.append(self.createFullSwap())
                self.swapNO += 1
            elif self.swapNO == self.swapsPerStreak[self.streak]:
                self.doneshuffling = True
                     
        for _, key_dict in self.keyPositions.items():
            self.draw_key(key_dict['_x'], key_dict['_y'], key_dict['color'])
            
    def move(self, ID: int, _x, _y) -> None:
    
        self.keyPositions[ID]['_x'] = _x
        self.keyPositions[ID]['_y'] = _y
        
    def initKeys(self):
        
        self.keyPositions[1] = {'_x': 50, '_y': 200, 'color': 'red', 'basePosition': 1}
        self.keyPositions[2] = {'_x': 175, '_y': 200, 'color': 'red', 'basePosition': 2}
        self.keyPositions[3] = {'_x': 300, '_y': 200, 'color': 'red', 'basePosition': 3}
        self.keyPositions[4] = {'_x': 425, '_y': 200, 'color': 'red', 'basePosition': 4}
        self.keyPositions[5] = {'_x': 550, '_y': 200, 'color': 'red', 'basePosition': 5}
        self.keyPositions[6] = {'_x': 50, '_y': 400, 'color': 'red', 'basePosition': 6}
        self.keyPositions[7] = {'_x': 175, '_y': 400, 'color': 'red', 'basePosition': 7}
        self.keyPositions[8] = {'_x': 300, '_y': 400, 'color': 'red', 'basePosition': 8}
        self.keyPositions[9] = {'_x': 425, '_y': 400, 'color': 'red', 'basePosition': 9}
        self.keyPositions[10] = {'_x': 550, '_y': 400, 'color': 'red', 'basePosition': 10}
          
    def createSwap(self, ID_1: int, ID_2: int, nf: int = 100) -> list[dict]:
        
        x_1: int = self.keyPositions[ID_1]['_x']
        x_2: int = self.keyPositions[ID_2]['_x']
        y_1: int = self.keyPositions[ID_1]['_y']
        y_2: int = self.keyPositions[ID_2]['_y']
        
        dx = (x_2 - x_1) / nf
        dy = (y_2 - y_1) / nf
        
        return SwapTask(ID_1, ID_2, x_1, x_2, y_1, y_2, dx, dy, nf)
        
    def start(self) -> None:
        
        self.gameLoopBool = True
        self.t = random.randint(1, 10)
        self.highlight(self.t)
        
        while self.gameLoopBool:
            
            self.updateKeys()
            self.win.update()
            
            if self.doneshuffling:
                self.verifyAnswer()
                
        self.makeFile()
                              
    def makeFile(self) -> None:
        
        with open('reward.txt', 'w', encoding='utf-8') as f:
            f.write("Here's your reward : 2CD1. This is part of nowi's code.\nYou've fought very well ! Keep going and don't miss on the little things c:\n\n")
            asciiart = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡖⠀⡔⠀⠀⠀⠀⠀⠰⡰⡀⠀⠀⢳⣄⠀⠀⠐⠆⠀⠀⠀⠀⠀⠐⢆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡔⠛⠛⢯⡉⠑⠒⡤⠊⠀⠀⠀⠀⠀⠀⡆⠀⠀⠀⣀⣀⡀⠤⠤⠤⠤⠤⠼⠤⢴⣃⡀⠀⠀⠀⠀⠀⢳⢱⡀⠀⠀⢳⡱⣄⠀⠀⠐⢄⠀⠀⠀⠀⠈⢣⠀⠀⠀⠀
⠀⠀⠀⠀⢠⠋⠀⠀⣀⣀⢳⣠⠎⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠒⠦⣄⠀⠈⡇⢣⠀⠀⠀⢣⠈⢦⠀⠀⠀⠑⢄⠀⠀⠀⠀⢣⡀⠀⠀
⠀⠀⠀⢠⣃⠴⠊⠉⢀⡴⡻⢹⠘⠢⢄⣀⣀⠴⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠢⣱⠈⡇⠀⠀⠈⣇⠀⢷⡀⠀⠀⠈⠳⡀⠀⠀⠀⢳⡀⠀
⠀⠀⢀⠏⠁⠀⠀⢠⠎⡰⠁⠘⡄⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣽⠀⠀⠀⢸⠀⢸⡵⡀⠀⠀⠀⠘⢆⠀⠀⠀⢣⠀
⠀⠀⡜⠀⠀⠀⢠⠏⢰⡇⠀⠀⢑⠜⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠄⠒⠒⠒⠒⠂⠤⢄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⡀⠀⠈⡆⢸⢇⢱⡀⠀⠀⠀⠈⢦⠀⠀⠈⠀
⠀⢠⠃⠀⠀⠀⡞⠀⣿⠁⠀⢠⠎⠀⠀⠀⠀⠀⠀⢀⡄⠀⠀⠀⠀⠀⠀⠄⠀⠀⠤⠤⣀⡈⠑⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢄⠀⡇⢸⢸⠀⢧⠀⠀⠀⠀⠈⢧⣀⠴⠊
⠀⠈⠀⠀⠀⢸⠁⢸⢸⠀⣰⠃⠀⠀⠀⠀⠀⠀⡴⠋⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠢⢄⠑⢄⠀⠀⠀⢦⠀⠀⠀⠀⠀⠀⠈⢦⡇⢸⠘⡄⠘⡆⠀⠀⣀⠴⠊⠁⢀⡰
⠀⠀⠀⠀⠀⡇⠀⡎⢸⢠⠃⠀⠀⠀⠀⠀⢀⡞⠀⢠⠖⠁⠀⢤⡀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠢⣵⣄⠀⠀⠳⡀⠀⠀⠀⠀⠀⠀⢳⡌⠀⡇⠀⢷⡠⠊⠁⠀⣠⡔⡏⡜
⠀⠀⠀⠀⢸⠀⠀⡇⢸⡎⠀⠀⠀⠀⠀⢀⡎⠀⡴⠁⠀⠀⠀⠀⢹⢦⡈⠦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢧⣄⠀⠹⡄⠀⠀⠀⠀⠀⠀⢻⣠⣃⡴⠋⠀⣠⠔⠊⠀⡇⢩⠞
⠀⠀⠀⠀⡏⠀⠀⡇⡸⠀⠀⠀⠀⠀⠀⡞⠀⡜⠁⠀⠀⠀⠀⠀⢸⡆⠛⠦⡈⠢⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢆⠀⠘⡄⠀⠀⠀⠀⠀⠀⢻⡊⠀⣠⠊⠁⠀⠀⡜⢰⡇⠀
⠀⠀⠀⢠⠃⠀⠀⣇⠇⠀⠀⠀⠀⠀⢰⠁⡸⠁⠀⠀⠀⠀⠀⠀⢸⠁⠀⠀⠈⠓⠬⡑⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢣⠀⠹⡀⠀⠀⠀⠀⢠⡀⢣⡜⠁⠀⠀⠀⢰⢱⠃⢸⠀
⠀⠀⠀⢸⠀⠀⠀⢹⢠⠀⠀⠀⠀⠀⢸⢠⠃⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠈⠑⠲⠭⣲⡴⢖⣒⡆⠀⠀⠀⠀⠀⢧⠀⢳⠀⠀⠀⠀⠀⢧⠈⡆⠀⠀⠀⢠⢇⠇⠀⠸⠀
⠀⠀⠀⡎⠀⠀⠀⡎⢸⠀⠀⠀⠀⠀⢿⡜⠀⠀⠀⠀⠀⠀⡀⠀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⢉⡡⠞⠛⢭⣭⣥⠤⠤⠚⡆⠈⣦⠆⠀⠀⠀⠸⠀⢳⠀⠀⠀⡞⡞⠀⠀⠀⠀
⠀⠀⠀⡇⠀⠀⢰⡇⢸⠀⠀⠀⠀⠀⢸⠇⠀⠀⠀⠀⠀⢠⡏⣸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⠉⠉⣠⠖⠋⠁⢀⣤⣤⣦⣔⣳⡾⢳⠀⠀⠀⠀⠀⡇⢸⣀⡠⠊⣼⢸⠀⠀⠀⠀
⠀⠀⠀⡇⠀⠀⢸⡇⢸⠀⠀⠀⠀⠀⠸⡀⠀⠀⠀⠀⢀⡮⣵⠓⢠⡤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡝⢀⣴⣯⣿⡿⣛⣿⣿⣻⡄⢸⠀⠀⠀⠀⢀⡇⠸⠣⣄⡜⠁⢸⠀⠀⠀⠀
⠀⠀⠀⡇⠀⠀⡇⠇⢸⠀⠀⠀⠀⠀⠀⣇⠀⠀⠀⢴⣱⣷⣁⢤⣊⣀⡀⠙⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⣨⡿⠁⢿⣄⡿⠟⣸⡛⡇⡎⠀⠀⠀⠀⢸⣵⢐⣴⠋⠀⠀⠈⠀⠀⠀⠀
⠯⣉⠀⠓⠒⠒⠃⢼⠸⡄⠀⠀⠀⠀⠀⠸⡀⠀⢀⣼⠏⡠⠞⠁⠀⠈⠙⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⠀⠀⠐⣲⡾⠏⠀⣧⢣⠀⠀⠀⠀⡎⣿⣼⢸⡆⠀⠀⠀⠀⠀⠀⠀
⠣⢌⡻⣍⣱⠒⡠⢼⠀⡇⠀⠀⠀⠀⠀⠀⢧⡠⠚⠁⠘⢁⣤⣶⣶⣶⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡟⢸⠀⠀⠀⢰⢹⡜⣿⣿⢣⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠉⢲⣄⡀⢣⡈⡇⢹⠀⠀⠀⠀⠀⢢⠘⡄⢄⣀⣠⣾⠟⢹⣏⡈⣿⡿⣿⠲⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀⢸⠀⠀⢠⢃⡏⡇⡿⣹⢸⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢸⣡⠉⡶⣍⢳⠀⣇⠀⠀⠀⠀⠈⣆⠻⣄⠀⠉⠙⢦⣀⠉⠹⠧⣤⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠁⠀⢸⠀⣠⠃⡞⡇⡇⠀⡟⡞⠁⠀⠀⠀⠀⢀⠀
⠀⠀⠀⠀⡿⠀⡇⠀⠹⡄⢸⡄⠀⠀⠀⠀⠘⡄⢣⠳⣄⠀⠀⠀⠋⠚⠙⠉⠁⠀⠀⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⢸⡰⠁⡜⠁⡗⢸⠀⢹⠃⠀⠃⠀⠀⠀⠸⠀
⠀⠀⠀⠀⢧⡇⠃⠀⠀⢳⠈⡿⡀⠀⠀⠀⠀⠘⣆⢳⡌⣢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢯⣼⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠜⢁⡞⠀⢰⠃⣼⠀⢸⠀⠀⠀⠀⠀⠀⡇⠀
⠀⠀⠀⠀⢸⢡⠀⠀⠀⠈⢧⢱⢱⡀⠀⠀⠀⠀⢹⢫⣫⡁⠑⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠃⠀⠀⠀⠀⠀⢀⡾⠁⠀⡜⢠⢻⠀⢸⠀⠠⠀⠀⠀⢠⠃⠀
⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠈⣎⢿⠙⣄⠀⠀⠀⠈⣿⢯⠳⣄⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⠐⠊⠁⠀⠀⠀⠀⠀⠀⡰⠋⠀⠀⣼⢥⠏⡸⠀⡎⡄⠀⠀⠀⠀⡸⠀⠀
⠀⠀⠀⠀⠀⢳⠀⠀⠀⠀⠀⢸⢞⣞⡞⢳⡀⠸⡄⠛⡌⣦⠏⠷⠄⠀⠑⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠀⠀⣠⡾⡿⠋⢀⡇⢀⢧⠃⠀⠀⠀⠀⡇⠀⠀
⠀⠀⠀⠀⠀⠸⡄⠀⠀⠀⠀⢸⢸⣿⣦⣞⠏⠢⣱⢀⢧⢹⠀⠀⠀⠀⠀⠀⠈⠉⠒⠒⠠⠤⠤⢀⣀⣀⣀⠀⠀⠀⢀⡠⠞⠁⢀⣠⣾⣿⢾⡀⠀⠘⠀⢸⡜⠀⠀⠀⠀⠘⠀⡸⠀
⠀⠀⠀⠀⠀⠀⢇⠀⠀⠀⠀⢸⢸⠿⡫⠋⠀⠀⠈⡟⠈⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢿⣿⢿⣿⠯⠥⠤⠒⣎⡿⢿⡿⠳⡀⠑⣄⠀⠀⣏⠃⠀⠀⠀⠀⠀⢠⠃⠀
⠀⠀⠀⠀⠀⠀⢸⡀⠀⠀⠀⢸⡈⠉⠀⠀⠀⠀⠀⠇⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢹⠍⢹⠉⢹⠀⠀⢀⣳⡄⠙⢄⠈⢢⣰⡻⠀⠀⠀⠀⠀⠀⡞⠀⠀
⠀⠀⠀⠀⠀⠀⠘⣇⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⢸⠀⣸⠎⠉⠓⠢⢜⣆⠈⢣⡀⢹⠇⠀⠀⠀⠀⠀⢠⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡿⡄⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠀⠈⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡃⢸⡴⢻⠀⣀⣠⣤⣶⣾⣧⡀⠑⡼⠀⠀⠀⠀⠀⠀⡸⠀⠀⠀
⠀⠀⡆⠀⠀⠀⠀⢸⢣⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠟⡇⢸⣟⢿⡿⠿⠿⠿⠛⣷⣄⡇⠀⠀⠀⠀⠀⠀⡇⠀⡴⠀
⠀⠀⢱⠀⠀⠀⠀⠈⡎⡆⠀⠀⡷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⡇⢸⡇⠀⠀⣀⡠⠤⠖⠛⠚⡇⠀⢠⠀⠀⠀⢠⠃⢰⠃⠀"""
            f.write(asciiart)
            f.write("\n\n(This is from frieren, the GREATEST anime of it's time.)")
            
    def verifyAnswer(self) -> None:
        
        self.freeze = True
        
        a = self.highlight_numbers()
        self.win.update()
        userInput: str = self.win.textinput("H3LL", "Entrez le numéro de la clé de départ :")
        
        try: 
            userInput = int(userInput)
        except ValueError: 
            userInput = 0
        
        
        if userInput == self.lookup_dict.get((self.keyPositions[self.t]['_x'], self.keyPositions[self.t]['_y']), None):
            
            self.streak += 1
            
            if self.streak == 3:
                self.gameLoopBool = False
            else:
                if self.streak == 1:
                    self.infoTurtle.clear()
                    self.infoTurtle.write(f"Pour l\'instant ça va hein ({self.streak})", font=("Arial", 20, "normal"))
                else:
                    self.infoTurtle.clear()
                    self.infoTurtle.write(f"vas y c bon si tu trouves c trop ({self.streak})", font=("Arial", 20, "normal"))
                
                self.doneshuffling = False
                self.swapNO = 0
                self.t = random.randint(1, 10)
                self.highlight(self.t)
        
        else:
            self.streak = 0
            self.swapNO = 0
            self.infoTurtle.clear()
            self.infoTurtle.write(f"nuh uh. Streak actuelle : {self.streak}", font=("Arial", 20, "normal"))
            self.doneshuffling = False
            self.t = random.randint(1, 10)
            self.highlight(self.t)
        
        a.clear()
        del a
        self.freeze = False
  
    def highlight(self, id: int) -> None:
        
        self.freeze = True
        
        for _ in range(5):
            
            self.keyPositions[id]['color'] = 'green'
            self.updateKeys()
            self.win.update()
            time.sleep(0.2)
            self.keyPositions[id]['color'] = 'red'
            self.updateKeys()
            self.win.update()
            time.sleep(0.2)
            
        self.freeze = False
            
    def createFullSwap(self) -> list[list[dict]]:
        
        full_swap_task: list = []
        for p in self.createPermutation():
            full_swap_task.append(self.createSwap(p[0], p[1], self.speed[self.streak]))
            
        return full_swap_task
  
    def highlight_numbers(self):
        
        self.freeze = True
        
        temp_turt = turtle.Turtle()
        temp_turt.hideturtle()
        
        for coord, data in self.lookup_dict.items():
            
            if data != 10: self.goto(temp_turt, coord[0] - 7, coord[1] - 5)
            else: self.goto(temp_turt, coord[0] - 13, coord[1] - 5)
            
            print(data, coord)
            temp_turt.write(f'{data}', font=("Arial", 20, "normal"))
            self.win.update()
        
        self.freeze = False
        return temp_turt
    
    @staticmethod
    def createPermutation():

        # quelques patternes acceptables
        right = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 10), (10, 9), (9, 8), (8, 7), (7, 6), (6, 1)]
        left = [(1, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 5), (5, 4), (4, 3), (3, 2), (2, 1)]
        semi_right = [(1, 2), (2, 7), (7, 6), (6, 1), (3, 8), (8, 3), (4, 5), (5, 10), (10, 9), (9, 4)]
        semi_left = [(4, 9), (9, 10), (10, 5), (5, 4), (3, 8), (8, 3), (1, 6), (6, 7), (7, 2), (2, 1)]
        
        return random.choice([semi_right, semi_left, right, left])
        
        

  
if __name__ == '__main__':
    
    instance = ShuffleGame()
    instance.start()
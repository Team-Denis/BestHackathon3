
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
            return ({'target': self.ID1,'ft': self.current_step,
                    'new_x': self.x1 + self._dx*self.current_step,'new_y': self.y1 + self._dy*self.current_step},
                    {'target': self.ID2,'ft': self.current_step,
                    'new_x': self.x2 - self._dx*self.current_step,'new_y': self.y2 - self._dy*self.current_step})
    
    def isDone(self) -> bool:
        return self.steps == self.current_step

class ShuffleGame:
    
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
        
        self.keyPositions: dict[int: dict] = dict()
        self.taskPriorityQueue: list[list[SwapTask]] = []
        self.initKeys()
        
    def goto(self, _x: int, _y: int) -> None:
        
        self.turtle.penup()
        self.turtle.goto(-self.width/2 + _x, self.height/2 - _y)
        self.turtle.pendown()
        
    def draw_key(self, _x, _y, color) -> None:
        
        self.goto(_x, _y)
        self.turtle.begin_fill()
        self.turtle.color(color)
        self.turtle.fillcolor(color)
        self.turtle.circle(20)
        self.turtle.end_fill()
    
    def updateKeys(self) -> None:
        
        self.turtle.clear()
        
        if self.taskPriorityQueue:
            if self.taskPriorityQueue[0]:
                for task in self.taskPriorityQueue[0]:
                    
                    p1, p2 = task.advanceStep()
                    self.move(p1['target'], p1['new_x'], p1['new_y'])
                    self.move(p2['target'], p2['new_x'], p2['new_y'])
                    if task.isDone():self.taskPriorityQueue[0].remove(task)
                    
            else:
                self.taskPriorityQueue.pop(0)
                print(self.keyPositions[1])
                     
        for _, key_dict in self.keyPositions.items():
            self.draw_key(key_dict['_x'], key_dict['_y'], key_dict['color'])
            
            
    def move(self, ID: int, _x, _y) -> None:
    
        self.keyPositions[ID]['_x'] = _x
        self.keyPositions[ID]['_y'] = _y
        
    def initKeys(self):
        
        self.keyPositions[1] = {'_x': 50, '_y': 200, 'color': 'red'}
        self.keyPositions[2] = {'_x': 175, '_y': 200, 'color': 'blue'}
        self.keyPositions[3] = {'_x': 300, '_y': 200, 'color': 'green'}
        self.keyPositions[4] = {'_x': 425, '_y': 200, 'color': 'yellow'}
        self.keyPositions[5] = {'_x': 550, '_y': 200, 'color': 'black'}
        self.keyPositions[6] = {'_x': 50, '_y': 400, 'color': 'gold'}
        self.keyPositions[7] = {'_x': 175, '_y': 400, 'color': 'purple'}
        self.keyPositions[8] = {'_x': 300, '_y': 400, 'color': 'cyan'}
        self.keyPositions[9] = {'_x': 425, '_y': 400, 'color': 'lime'}
        self.keyPositions[10] = {'_x': 550, '_y': 400, 'color': 'pink'}
        
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
        
        for _ in range(10):
            self.taskPriorityQueue.append(self.createFullSwap())
        
        while self.gameLoopBool:
            
            self.updateKeys()
            self.win.update()
            
    
    def createFullSwap(self) -> list[list[dict]]:
        
        full_swap_task: list = []
        for p in self.createPermutation(10):
            full_swap_task.append(self.createSwap(p[0], p[1], 600))
            
        
        return full_swap_task
            
    @staticmethod
    def createPermutation(n: int):

        t = [i for i in range(1, n+1)]
        random.shuffle(t)
        return [(t[i], t[i+1]) for i in range(0, len(t), 2)]
        
        
        
        
# Full swap contient des liste de swap_task, qui contiennent des listes de tuple 
        
        
if __name__ == '__main__':
    
    instance = ShuffleGame()
    instance.start()
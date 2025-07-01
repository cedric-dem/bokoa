

class Game(object):
    def __init__(self,level):
        self.level=level
        self.score=1
        self.grid_size=level.grid_size

        self.moves_history=[]
        self.position_history=[[0,0]]
    
    def move(self,direction,new_pos):
        self.moves_history.append(direction)

        new_operation=self.level.level[new_pos[0]][new_pos[1]]

        self.apply_operation(new_operation)

        self.position_history.append(new_pos)

    def apply_operation(self,operation):
        if operation[0]=='+':
            self.score+=int(operation[1])

        elif operation[0]=='-':
            self.score-=int(operation[1])

        elif operation[0]=='×':
            self.score*=int(operation[1])

        elif operation[0]=='÷':
            self.score/=int(operation[1])


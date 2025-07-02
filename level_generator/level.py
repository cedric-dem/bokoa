import random

class Level(object):
    def __init__(self,grid_size):
        self.grid_size=grid_size

        self.create_level()
    
    def create_level(self):

        total_of_each_op=((self.grid_size[0]*self.grid_size[1]))//4
        raw=['+' for i in range (total_of_each_op)]+['-' for i in range (total_of_each_op)]+['×' for i in range (total_of_each_op)]+['÷' for i in range (total_of_each_op)]
        
        if self.grid_size==[4,4] or self.grid_size==[5,6]:
            raw+=["+"]
        
        random.shuffle(raw)

        self.level=[[None for i in range (self.grid_size[0])] for j in range (self.grid_size[1])]
        
        
        for i in range (self.grid_size[0]):
            for j in range (self.grid_size[1]):
                if i==0 and j==0:
                    self.level[0][0]="1"
                else:
                    if raw[0]=="×" or raw[0]=="÷":
                        tmp=raw[0]+str(random.randint(2,5))
                        
                    else:
                        tmp=raw[0]+str(random.randint(1,5))
                        
                    self.level[j][i]=tmp
                    del raw[0]


    def displayLevel(self):
        for line in self.level:
            print(line)

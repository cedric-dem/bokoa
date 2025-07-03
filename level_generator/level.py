import random

random.seed(123456789)

def get_operations_reserve(grid_size):
    total_of_each_op = (grid_size[0] * grid_size[1]) // 4
    operations_reserve = (
            ['+' for _ in range(total_of_each_op)] +
            ['-' for _ in range(total_of_each_op)] +
            ['×' for _ in range(total_of_each_op)] +
            ['÷' for _ in range(total_of_each_op)])

    if grid_size == [4, 4] or grid_size == [5, 6]:
        operations_reserve += ["+"]
    random.shuffle(operations_reserve)
    return operations_reserve

class Level(object):
    def __init__(self,grid_size):
        self.grid_size=grid_size

        self.create_level()
    
    def create_level(self):

        operations_reserve=get_operations_reserve(self.grid_size)

        self.level=[[None for _ in range (self.grid_size[0])] for _ in range (self.grid_size[1])]
        
        for i in range (self.grid_size[0]):
            for j in range (self.grid_size[1]):
                if i==0 and j==0:
                    self.level[0][0]="1"
                else:
                    if operations_reserve[0]=="×" or operations_reserve[0]=="÷":
                        new_operation=operations_reserve[0]+str(random.randint(2,5))
                        
                    else:
                        new_operation=operations_reserve[0]+str(random.randint(1,5))
                        
                    self.level[j][i]=new_operation
                    del operations_reserve[0]

    def display_level(self):
        for line in self.level:
            print(line)
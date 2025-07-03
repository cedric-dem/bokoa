from game import Game
from config import *

def get_direction(move):
    if move==">": #good
        result=[0,1]
        
    elif move=="<":
        result=[0,-1]
        
    elif move=="u":
        result=[1,0]
    
    elif move=="n":
        result=[-1,0]
    
    return result
    
class LevelWithSol(object):
    def __init__(self,level,best_score,best_moves):
        self.level=level
        self.best_score=best_score
        self.best_moves=best_moves
        self.historyOfScores=None
        self.grid_size=level.grid_size
    
    def set_fitness_score(self):
        self.historyOfScores=[1]
        current_game=Game(self.level)

        decreasing_steps_counter=0
        increasing_steps_counter=0

        found_first_neg=False
        found_first_pos=False

        consecutive_first_steps_diminish=0

        total_score_decreasing=0
        total_score_increasing=0
        
        for move in self.best_moves:
            old_score=current_game.score

            move_direction=get_direction(move)
            current_position=current_game.position_history[-1]
            new_position=[current_position[0]+move_direction[0], current_position[1]+move_direction[1]]
            current_game.move(move_direction,new_position)
            
            self.historyOfScores.append(current_game.score)
            new_score=current_game.score

            if new_score>old_score:
                found_first_pos=True
                increasing_steps_counter+=1
                total_score_increasing+=(new_score-old_score)

            if new_score<old_score:
                if not found_first_pos:
                    consecutive_first_steps_diminish+=1

                total_score_decreasing+=(old_score-new_score)
                decreasing_steps_counter+=1

        ####################################################################################################################

        if self.grid_size[0]==4:
            k1=2.0998
            k2=2.34
            k3=1.21

        elif self.grid_size[0]==5:
            k1=2.332
            k2=2.666
            k3=0.626

        elif self.grid_size[0]==6:
            k1=1.92
            k2=2.026
            k3=0.743

        t1 = k1 - (k2 * (increasing_steps_counter / (len(self.historyOfScores))))
        t2 = (total_score_decreasing / self.historyOfScores[-1]) / k3

        self.fitness= (coefficient_second_term * t2) + (t1)

    def display_everything(self):
        self.level.display_level()
        print(self.best_moves)
        print(self.best_score)

    def __gt__(self,other):
        return (self.fitness>other.fitness) 

    def __eq__(self,other):
        return (self.fitness==other.fitness) 

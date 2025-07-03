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
    
class LevelWithSolution(object):
    def __init__(self,level,best_score,best_moves):
        self.level=level

        self.best_score=best_score
        self.best_moves=best_moves

        self.historyOfScores=None

        self.grid_size_id=level.grid_size_id
        self.grid_size=level.grid_size
    
    def set_fitness_score(self):
        self.historyOfScores=[1]
        current_game=Game(self.level)

        increasing_steps_counter=0

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
                increasing_steps_counter+=1
                total_score_increasing+=(new_score-old_score)

            if new_score<old_score:
                total_score_decreasing+=(old_score-new_score)

        fitness_first_term = coefficient_fitness_first_term_a[self.grid_size_id] - (coefficient_fitness_first_term_b[self.grid_size_id] * (increasing_steps_counter / (len(self.historyOfScores))))
        fitness_second_term = (total_score_decreasing / self.historyOfScores[-1]) / coefficient_fitness_second_term_a[self.grid_size_id]

        self.estimated_difficulty= (coefficient_fitness_second_term * fitness_second_term) + fitness_first_term

    def display_everything(self):
        print('==> Grid :')
        self.level.display_level()
        print('==> Solution :',self.best_moves)
        print('==> Best Score : ',self.best_score)

    def __gt__(self,other):
        return self.estimated_difficulty>other.estimated_difficulty

    def __eq__(self,other):
        return self.estimated_difficulty==other.estimated_difficulty

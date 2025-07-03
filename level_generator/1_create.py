
from backtrack import back_track
from game import Game
from levelWithSol import LevelWithSol
from level import Level
import pickle
import time
from config import *

def get_readable_moves(moves_list):
    result=[]
    for move in moves_list:
        if move==[0,-1]:
            result.append('<')

        elif move==[0,1]:
            result.append('>')

        elif move==[1,0]:
            result.append('u')

        elif move==[-1,0]:
            result.append('n')

    return result

def create_one_level(grid_size, fn):
    ##create level
    temp_level=Level(grid_size)
    
    ##create game
    temp_game=Game(temp_level)
    
    ##do the backtrack
    best_score, best_moves = back_track(temp_game, grid_size[0] * grid_size[1])

    #create level with solution
    lws=LevelWithSol(temp_level, best_score, get_readable_moves(best_moves))

    #save level with solution
    temp=open(fn,"wb")
    pickle.dump(lws, temp)

    #debug
    if (display_new_levels):
        temp_level.display_level()
        print("Best sol : ",best_score,get_readable_moves(best_moves))
        lws.display_everything()
        print("=======================================================================")

    return best_score
    
def create_levels():
    for grid_size_id in grid_sizes_id:
        grid_size=grid_sizes[grid_size_id]
        prefix=file_prefixes_raw[grid_size_id]

        print("Currently on size ",grid_size," prefix", prefix )

        t0=time.time()

        for i in range (raw_levels_to_generate):
            print("==> generate level",i)
            this_score=create_one_level(grid_size, prefix + str(i))
            print( i + 1,"/", raw_levels_to_generate, " finished. Score : ", this_score)

        t1=time.time()

        print("Time taken : " + str((t1-t0) / raw_levels_to_generate) + ' seconds per it')

create_levels()
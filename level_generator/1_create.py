
from backtrack import back_track
from game import Game
from level import Level
import time
from misc import *

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

def create_one_level(grid_size_id, fn):
    # create level
    temp_level=Level(grid_size_id, None)
    
    # create game
    temp_game=Game(temp_level)
    
    # do the backtrack
    grid_size=grid_sizes[grid_size_id]
    best_score, best_moves = back_track(temp_game, grid_size[0] * grid_size[1])

    # save level with solution as json
    create_level_file_as_json(temp_level.operations_grid, best_score, get_readable_moves(best_moves), fn)

def create_levels():
    for grid_size_id in grid_sizes_id:
        grid_size=grid_sizes[grid_size_id]
        prefix=get_file_prefix_complete(grid_size_id)

        print("Currently on size ",grid_size," prefix", prefix )

        t0=time.time()

        for current_level_index in range (raw_levels_to_generate):
            print("==> generate level",current_level_index)
            create_one_level(grid_size_id, prefix + str(current_level_index)+".json")
            print( current_level_index + 1,"/", raw_levels_to_generate, " finished")

        t1=time.time()

        print("Time taken : " + str((t1-t0) / raw_levels_to_generate) + ' seconds per it')

create_levels()
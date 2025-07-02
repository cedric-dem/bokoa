from backtrack import backTrack
from game import Game
from levelWithSol import LevelWithSol
from level import Level
import pickle
import time
from config import *

offset=0



def getReadableMoves(lm):
    res=[]
    for move in lm:
        if move==[0,-1]:
            res.append('<')

        elif move==[0,1]:
            res.append('>')

        elif move==[1,0]:
            res.append('u')

        elif move==[-1,0]:
            res.append('n')

    return res

def createOneLevel(grid_size, fn):
    ##create level
    lv=Level(grid_size)
    
    ##create game
    gm=Game(lv)
    
    ##do the backtrack
    best_score, best_moves = backTrack(gm,grid_size[0]*grid_size[1])

    #create levelwithsol
    lws=LevelWithSol(lv, best_score, getReadableMoves(best_moves))

    #save levelwithsol
    temp=open(fn,"wb")
    pickle.dump(lws, temp)
    

    #debug
    """
    lv.displayLevel()
    print("Best sol : ",best_score,getReadableMoves(best_moves))
    lws.printGf()
    print("=======================================================================")
    """
    return best_score
    

for grid_size in all_grid_sizes:
    if (grid_size[0]==4):
        prefix="generated_levels/raw/levels_0/level_"

    elif (grid_size[0]==5):
        prefix="generated_levels/raw/levels_1/level_"

    elif (grid_size[0]==6):
        prefix="generated_levels/raw/levels_2/level_"

    print("Currently on size ",grid_size," prefix", prefix )


    t0=time.time()

    for i in range (raw_levels_to_generate):
        print("==> generate level",i)
        this_score=createOneLevel(grid_size, prefix + str(offset + i))
        print(offset + i + 1,"/", raw_levels_to_generate, " finished. Score : ", this_score)


    t1=time.time()

    print("Time taken : " + str((t1-t0) / (raw_levels_to_generate)) + ' seconds per it')

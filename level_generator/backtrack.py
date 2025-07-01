def isMoveInBound(gm,new_pos):
    return (new_pos[0]>=0 and  new_pos[1]>=0 and new_pos[0]<gm.grid_size[1]  and   new_pos[1]<gm.grid_size[0])

def isMoveInSnake(gm,new_pos):
    return (new_pos in gm.position_history)

def getAllButInverseOfLastMove(gm):
    if len(gm.moves_history)==0:
        return [[0,-1],[0,1],[1,0],[-1,0]]

    elif gm.moves_history[-1]==[1,0]:
        return [[0,-1],[0,1],[1,0]]

    elif gm.moves_history[-1]==[-1,0]:
        return [[0,-1],[0,1],[-1,0]]

    elif gm.moves_history[-1]==[0,-1]:
        return [[0,-1],[1,0],[-1,0]]

    elif gm.moves_history[-1]==[0,1]:
        return [[0,1],[1,0],[-1,0]]

    else:
        print('YEET')
        return None

def backTrack(gm,max_depth):

    if 1<gm.score:
        best_score=gm.score
        best_moves=gm.moves_history[::]

    else:
        best_score=1
        best_moves=[]

    
    if len(gm.moves_history)<max_depth:  #else stop
        for new_move in  getAllButInverseOfLastMove(gm):

            new_pos=[gm.position_history[-1][0]+new_move[0],gm.position_history[-1][1]+new_move[1]]

            ##if move ok + not coming back
            if (isMoveInBound(gm,new_pos) and (not isMoveInSnake(gm,new_pos))):
                #save old score
                old_score=gm.score
            
                #move
                gm.move(new_move,new_pos)

                #launch backtrack
                temp_best_score,temp_best_moves=backTrack(gm,max_depth)

                ##restore old state
                gm.score=old_score
                gm.moves_history.pop()
                gm.position_history.pop()


                if (best_score<temp_best_score):  #if new res better than prev:
                    #best_score and best_moves refresh
                    best_score=temp_best_score
                    best_moves=temp_best_moves[::]
                    
    return best_score,best_moves

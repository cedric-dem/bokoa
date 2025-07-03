def is_move_in_bound(gm, new_pos):
    return new_pos[0]>=0 and  new_pos[1]>=0 and new_pos[0]<gm.grid_size[1] and new_pos[1]<gm.grid_size[0]

def is_move_in_history(gm, new_pos):
    return new_pos in gm.position_history

def get_all_but_inverse_of_last_move(gm):
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
        print('Error')
        return None

def back_track(game, max_depth):

    if 1<game.score:
        best_score=game.score
        best_moves= game.moves_history[::]

    else:
        best_score=1
        best_moves=[]
    
    if len(game.moves_history)<max_depth:  #else stop
        for new_move in  get_all_but_inverse_of_last_move(game):

            new_pos=[game.position_history[-1][0] + new_move[0], game.position_history[-1][1] + new_move[1]]

            ##if move ok + not coming back
            if is_move_in_bound(game, new_pos) and (not is_move_in_history(game, new_pos)):
                #save old score
                old_score=game.score
            
                #move
                game.move(new_move, new_pos)

                #launch backtrack
                temp_best_score,temp_best_moves=back_track(game, max_depth)

                ##restore old state
                game.score=old_score
                game.moves_history.pop()
                game.position_history.pop()

                if best_score<temp_best_score:  #if new res better than prev:
                    #best_score and best_moves refresh
                    best_score=temp_best_score
                    best_moves=temp_best_moves[::]
                    
    return best_score,best_moves

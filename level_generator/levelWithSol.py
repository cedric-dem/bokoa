from game import Game

def getDirection(move):
    if move==">": #good
        res=[0,1]
        
    elif move=="<":
        res=[0,-1]
        
    elif move=="u":
        res=[1,0]
    
    elif move=="n":
        res=[-1,0]
    
    return res
    
class LevelWithSol(object):
    def __init__(self,level,best_score,best_moves):
        self.level=level
        self.best_score=best_score
        self.best_moves=best_moves
        self.historyOfScores=None
        self.grid_size=level.grid_size
    
    def setFitnessScore(self):
        self.historyOfScores=[1]
        gm=Game(self.level)

        decreasing_ctr=0
        increasing_ctr=0

        found_first_neg=False
        found_first_pos=False

        consecutive_first_steps_diminish=0

        total_diminution=0
        total_augmentation=0

        
        for move in self.best_moves:
            old_score=gm.score

            d=getDirection(move)
            current_pos=gm.position_history[-1]
            new_pos=[current_pos[0]+d[0], current_pos[1]+d[1]]
            gm.move(d,new_pos)
            
            self.historyOfScores.append(gm.score)
            new_score=gm.score

            if (new_score>old_score):
                found_first_pos=True
                increasing_ctr+=1
                total_augmentation+=(new_score-old_score)

            if (new_score<old_score):
                if not found_first_pos:
                    consecutive_first_steps_diminish+=1

                total_diminution+=(old_score-new_score)
                decreasing_ctr+=1
                if not found_first_neg:
                    found_first_neg=True
                    first_neg=len(self.historyOfScores)

        if not found_first_neg:
            first_neg=len(self.historyOfScores)

        ####################################################################################################################

        if self.grid_size[0]==4:
            t1=2.0998-(2.34*(increasing_ctr/(len(self.historyOfScores))))
            t2=(total_diminution/self.historyOfScores[-1])/1.21

        elif self.grid_size[0]==5:
            t1=2.332-(2.666*(increasing_ctr/(len(self.historyOfScores))))
            t2=(total_diminution/self.historyOfScores[-1])/0.626

        elif self.grid_size[0]==6:
            t1=1.92-(2.026*(increasing_ctr/(len(self.historyOfScores))))
            t2=(total_diminution/self.historyOfScores[-1])/0.743


        self.fitness=(1.5*t2)+(t1)


    def printGf(self):
        self.level.displayLevel()
        print(self.best_moves)
        print(self.best_score)
    
    def getGoodFormat(self):

        ## Level itself
        res='new Level(new String[][] {'
        for i in range (self.grid_size[1]):

            res=res+"{"
            
            for j in self.level.level[i]:
                res=res+'"'+j+'",'

            if i!=self.grid_size:
                res=res+"}, "
            else:
                res=res+"}"
            
        res=res+'}, '
        
        ## max score : 
        res=res+str(round(self.best_score,2))+'F, '

        ## best sol
        res=res+'new String[] {'
        for mov in self.best_moves:
            res=res+'"'+str(mov)+'", '
        res=res+'}),'

        return res


    def __gt__(self,other):
        return (self.fitness>other.fitness) 

    def __eq__(self,other):
        return (self.fitness==other.fitness) 

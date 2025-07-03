import pickle
import json
from config import *


def createLevelFileAsJson(l, filename):
    result={
        "operations":l.level.level,
        "bestScore":round(float(l.best_score),2),
        "bestMoves":l.best_moves
    }

    with open(filename, 'w') as file:
        json.dump(result, file, indent=4, separators=(',', ': '), ensure_ascii=False)
        print("done", filename)


for difficulty in difficulties:

    print('====> Current difficulty', difficulty)

    # =========================================================================== blabla

    size = all_grid_sizes[difficulty][0]

    # =========================================================================== get data
    L_all = []

    ##open all the files, put in a list
    for final_index_level in range(number_levels_to_keep):
        file = open(file_prefixes_processed[difficulty] + str(final_index_level), 'rb')
        data = pickle.load(file)

        createLevelFileAsJson(data, file_prefixes_processed_as_json[difficulty] + str(final_index_level) + ".json")
        #L_all.append(data)

    #print('===> ',len(L_all))
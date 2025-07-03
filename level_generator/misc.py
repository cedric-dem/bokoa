import json
from config import *

def create_level_file_as_json(operations, best_score, best_moves, filename):
    result={
        "operations":operations,
        "bestScore":round(float(best_score),2),
        "bestMoves":best_moves
    }

    with open(filename, 'w') as file:
        json.dump(result, file, indent=4, separators=(',', ': '), ensure_ascii=False)


def get_file_prefix_complete(difficulty_index):
    return generated_levels_folder_name + "/"+complete_folder_name+"/"+grid_size_folder_prefix+str(difficulty_index)+"/"+level_file_name

def get_file_prefix_reduced(difficulty_index):
    return generated_levels_folder_name + "/" + reduced_folder_name + "/" + grid_size_folder_prefix + str(difficulty_index) + "/" + level_file_name

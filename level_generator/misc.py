
import json


def create_level_file_as_json(operations, best_score, best_moves, filename):
    result={
        "operations":operations,
        "bestScore":round(float(best_score),2),
        "bestMoves":best_moves
    }

    with open(filename, 'w') as file:
        json.dump(result, file, indent=4, separators=(',', ': '), ensure_ascii=False)



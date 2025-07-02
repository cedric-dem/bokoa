raw_levels_to_generate=1000

number_levels_to_keep=100

all_grid_sizes=[[4,4],[5,5],[6,6]]

difficulties = [i for i in range (len(all_grid_sizes))]

file_prefixes_raw=[
    "generated_levels/raw/levels_0/level_",
    "generated_levels/raw/levels_1/level_",
    "generated_levels/raw/levels_2/level_"
]

file_prefixes_processed=[
    "generated_levels/processed/difficulty_0/level_",
    "generated_levels/processed/difficulty_1/level_",
    "generated_levels/processed/difficulty_2/level_"
]


file_prefixes_processed_as_json=[
    "generated_levels/processed_json/difficulty_0/level_",
    "generated_levels/processed_json/difficulty_1/level_",
    "generated_levels/processed_json/difficulty_2/level_"
]
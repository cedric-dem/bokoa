raw_levels_to_generate=1000

number_levels_to_keep=100

grid_sizes=[[4, 4], [5, 5], [6, 6]]

grid_sizes_id = [i for i in range (len(grid_sizes))]

file_prefixes_raw=[
    "generated_levels/raw/grid_size_0/level_",
    "generated_levels/raw/grid_size_1/level_",
    "generated_levels/raw/grid_size_2/level_"
]

file_prefixes_processed=[
    "generated_levels/processed/grid_size_0/level_",
    "generated_levels/processed/grid_size_1/level_",
    "generated_levels/processed/grid_size_2/level_"
]

file_prefixes_processed_as_json=[
    "generated_levels/processed_json/grid_size_0/level_",
    "generated_levels/processed_json/grid_size_1/level_",
    "generated_levels/processed_json/grid_size_2/level_"
]
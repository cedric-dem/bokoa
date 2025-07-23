package com.slykos.bokoa

object Config {
    const val MOVE_THRESHOLD = 100

    const val BLUE_VALUE_INITIAL = 80
    const val CASE_CENTER_WEIGHT = 0.9f
    const val CORNER_RADIUS_ONE_CORNER = 30f
    const val CORNER_RADIUS_TWO_CORNERS = 30f
    const val CORNER_RADIUS_FOUR_CORNERS = 30f

    const val AD_ID = "ca-app-pub-3940256099942544/5224354917" // fake ad, to replace with real one when publishing update

    const val LEVELS_SELECTION_ROWS = 20
    const val LEVELS_SELECTION_COLUMNS = 5

    const val NUMBER_OF_DIFFICULTIES = 3
    const val LEVELS_PER_DIFFICULTIES = 100

    val DIFFICULTIES_NAMES = arrayOf(
        "4x4",
        "5x5",
        "6x6"
    )

    val GRID_SIZES = arrayOf(
        intArrayOf(4, 4),
        intArrayOf(5, 5),
        intArrayOf(6, 6)
    )

    /// Debug
    const val PASS_ALL_LEVELS = false
    const val SKIP_AD = false
    const val SHOW_SOLUTION_AT_START = false
}
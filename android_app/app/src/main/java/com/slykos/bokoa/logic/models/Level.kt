package com.slykos.bokoa.logic.models

class Level(
    @JvmField var operations: Array<Array<Operation>> = arrayOf(),
    @JvmField var bestScore: Double = 0.0,
    @JvmField var bestMoves: Array<String> = arrayOf()
)

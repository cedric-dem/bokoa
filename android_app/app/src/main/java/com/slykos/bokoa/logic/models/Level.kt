package com.slykos.bokoa.logic.models

class Level(
    @JvmField var operations: Array<Array<Operation>> = arrayOf(),
    @JvmField var bestScore: Float = 0f,
    @JvmField var bestMoves: Array<String> = arrayOf()
)

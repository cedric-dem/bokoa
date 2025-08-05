package com.slykos.bokoa.logic.services

import com.slykos.bokoa.logic.game.Game
import com.slykos.bokoa.logic.models.Level
import com.slykos.bokoa.logic.models.MoveResult

class MovementHandler(
    private var gridSize: IntArray,
    private var game: Game
) {

    private var coordinatesHistory: MutableList<IntArray> = mutableListOf()

    fun start() {
        coordinatesHistory = mutableListOf(intArrayOf(0, 0))
        //maybe put that in init ?
    }

    private fun detectSituation(newCoordinate: IntArray): MoveResult =
        when {
            isOutsideBounds(newCoordinate) -> MoveResult.IMPOSSIBLE // outside bounds, not possible
            isMoveComingBack(newCoordinate) -> MoveResult.COME_BACK // coming back one step
            isCollidingWithPreviousCase(newCoordinate) -> MoveResult.IMPOSSIBLE // coming back more than one step, not possible
            else -> MoveResult.NORMAL // normal move
        }

    fun areCoordinatesEqual(coordinatesA: IntArray, coordinatesB: IntArray): Boolean =
        (coordinatesA[0] == coordinatesB[0] && coordinatesA[1] == coordinatesB[1])

    private fun isOutsideBounds(newCoordinate: IntArray): Boolean =
        (newCoordinate[0] < 0 || newCoordinate[0] >= gridSize[1] || newCoordinate[1] < 0 || newCoordinate[1] >= gridSize[0])

    private fun isMoveComingBack(newCoordinate: IntArray): Boolean =
        coordinatesHistory.size >= 2 && areCoordinatesEqual(
            coordinatesHistory[coordinatesHistory.size - 2],
            newCoordinate
        )

    private fun isCollidingWithPreviousCase(newCoordinate: IntArray): Boolean =
        coordinatesHistory.any { areCoordinatesEqual(it, newCoordinate) }

    private fun getLastPosition(): IntArray =
        coordinatesHistory.last()

    fun detectCaseAndMove(direction: IntArray) {
        val oldCoordinate = getLastPosition()
        val newCoordinate = intArrayOf(oldCoordinate[0] + direction[0], oldCoordinate[1] + direction[1])

        detectSituation(newCoordinate)
            .takeIf { it != MoveResult.IMPOSSIBLE }
            ?.run {
                applyMoveResult(this, oldCoordinate, newCoordinate)
            }
    }

    private fun applyMoveResult(moveResult: MoveResult, oldCoordinate: IntArray, newCoordinate: IntArray) {
        if (moveResult == MoveResult.NORMAL) {
            applyNormalMove(newCoordinate)

        } else {
            applyGoBackMove(oldCoordinate, newCoordinate)
        }

        game.refreshScoreVisual()
    }

    private fun applyNormalMove(newCoordinate: IntArray) {
        // append new coordinates to history
        coordinatesHistory.add(newCoordinate)
        game.movementReachNew(newCoordinate) // go for new
    }

    private fun applyGoBackMove(oldCoordinate: IntArray, newCoordinate: IntArray) {
        game.applyOperationOnScore(oldCoordinate) // coming back
        coordinatesHistory.removeAt(coordinatesHistory.lastIndex)
        game.gameMovementGoBack(oldCoordinate, newCoordinate) // coming back
    }

    fun getHistorySize(): Int =
        coordinatesHistory.size

    private fun getOlderPosition(distance: Int): IntArray =
        getCoordinateAtPosition(getHistorySize() - distance)

    fun getEntireHistory(): MutableList<IntArray> =
        coordinatesHistory

    fun getCoordinateAtPosition(i: Int): IntArray =
        coordinatesHistory[i]

    fun getLastMove(): IntArray =
        getMoveAtGivenPosition(getHistorySize() - 1)

    private fun getMoveAtGivenPosition(position: Int): IntArray {
        val positionA = getCoordinateAtPosition(position)
        val positionB = getCoordinateAtPosition(position - 1)

        return intArrayOf(
            positionA[0] - positionB[0],
            positionA[1] - positionB[1]
        )
    }

    private fun isMoveInDirection(direction: String, move: IntArray): Boolean =
        when (direction) {
            "u" -> areCoordinatesEqual(move, intArrayOf(1, 0))
            ">" -> areCoordinatesEqual(move, intArrayOf(0, 1))
            "n" -> areCoordinatesEqual(move, intArrayOf(-1, 0))
            "<" -> areCoordinatesEqual(move, intArrayOf(0, -1))
            else -> false // invalid direction
        }

    fun isOnGoodPath(currentLevel: Level): Boolean {
        var correctUntilNow = true

        if (getHistorySize() - 1 > currentLevel.bestMoves.size) {
            correctUntilNow = false
        } else {
            // go trough history
            for (i in 1 until getHistorySize()) {
                if (!isMoveInDirection(currentLevel.bestMoves[i - 1], getMoveAtGivenPosition(i))) {
                    correctUntilNow = false
                }
            }
        }
        return correctUntilNow
    }
}
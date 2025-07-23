package com.slykos.bokoa.models.game

import com.slykos.bokoa.R
import com.slykos.bokoa.pagesHandler.playPages.TutorialPageHandler

class TutorialGame(
    private var callingPage: TutorialPageHandler
) :
    Game(
        callingPage
    ) {

    override fun refreshScore() {
        super.refreshScore()

        setTipGiver()
        setEquationAndScoreViewer()
    }

    private fun isMoveInDirection(direction: String, move: IntArray): Boolean =
        when (direction) {
            "u" -> areCoordinatesEqual(move, intArrayOf(1, 0))
            ">" -> areCoordinatesEqual(move, intArrayOf(0, 1))
            "n" -> areCoordinatesEqual(move, intArrayOf(-1, 0))
            "<" -> areCoordinatesEqual(move, intArrayOf(0, -1))
            else -> false // invalid direction
        }

    private fun isOnGoodPath(): Boolean {
        var correctUntilNow = true
        var lastMove: IntArray

        if (coordinatesHistory.size - 1 > currentLevel.bestMoves.size) {
            correctUntilNow = false
        } else {
            // go trough history
            for (i in 1 until coordinatesHistory.size) {
                lastMove = intArrayOf(coordinatesHistory[i][0] - coordinatesHistory[i - 1][0], coordinatesHistory[i][1] - coordinatesHistory[i - 1][1])

                if (!isMoveInDirection(currentLevel.bestMoves[i - 1], lastMove)) {
                    correctUntilNow = false
                }
            }
        }
        return correctUntilNow
    }

    private fun getOppositeOfPreviousMove(): String {
        // TODO refactor this function (more generally the way of handling moves)

        val lastMove = intArrayOf(
            coordinatesHistory[coordinatesHistory.size - 2][0] - coordinatesHistory[coordinatesHistory.size - 1][0],
            coordinatesHistory[coordinatesHistory.size - 2][1] - coordinatesHistory[coordinatesHistory.size - 1][1]
        )

        return when {
            areCoordinatesEqual(lastMove, intArrayOf(-1, 0)) -> callingPage.resources.getString(R.string.move_up_string)
            areCoordinatesEqual(lastMove, intArrayOf(0, -1)) -> callingPage.resources.getString(R.string.move_left_string)
            areCoordinatesEqual(lastMove, intArrayOf(0, 1)) -> callingPage.resources.getString(R.string.move_right_string)
            areCoordinatesEqual(lastMove, intArrayOf(1, 0)) -> callingPage.resources.getString(R.string.move_down_string)
            else -> error("Next move not found")
        }
    }

    private fun getNextMove(): String =
        currentLevel.bestMoves.getOrNull(coordinatesHistory.size - 1)?.let { move ->
            when (move) {
                "u" -> callingPage.resources.getString(R.string.move_down_string)
                "n" -> callingPage.resources.getString(R.string.move_up_string)
                ">" -> callingPage.resources.getString(R.string.move_right_string)
                "<" -> callingPage.resources.getString(R.string.move_left_string)
                else -> error("Next move not found")
            }
        } ?: ""

    private fun setTipGiver() {
        callingPage.setTip(
            if (isOnGoodPath()) {
                if (coordinatesHistory.size == 1) {
                    callingPage.resources.getString(R.string.swipe) + getNextMove()
                } else {
                    callingPage.resources.getString(R.string.good_swipe) + getNextMove()
                }
            } else {
                callingPage.resources.getString(R.string.bad_swipe) + getOppositeOfPreviousMove()
            }
        )
    }

    private fun setEquationAndScoreViewer() {
        if (coordinatesHistory.size == 1) { // could remove if as already in for
            callingPage.setEquation("")
            callingPage.setCurrentScore("1")
        } else {
            var currentEquation = "1"

            var currentOperation: String

            for (i in coordinatesHistory.indices) {
                currentOperation = currentLevel.operations[coordinatesHistory[i][0]][coordinatesHistory[i][1]]

                currentEquation = when (i) {
                    0 -> "1"
                    1 -> "$currentEquation$currentOperation"
                    else -> "($currentEquation)$currentOperation"
                }
            }
            callingPage.setEquation("$currentEquation\n=")
            callingPage.setCurrentScore(getFormattedScore(currentScore))
        }
    }
}

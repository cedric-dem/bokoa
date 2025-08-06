package com.slykos.bokoa.logic.game

import com.slykos.bokoa.R
import com.slykos.bokoa.frontend.pages.playPages.TutorialPageHandler

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

    private fun getOppositeOfPreviousMove(): String {
        // TODO refactor this function (more generally the way of handling moves)
        val lastMove = movementHandler.getLastMove()

        return when {
            movementHandler.areCoordinatesEqual(lastMove, intArrayOf(1, 0)) -> callingPage.resources.getString(R.string.move_up_string)
            movementHandler.areCoordinatesEqual(lastMove, intArrayOf(0, 1)) -> callingPage.resources.getString(R.string.move_left_string)
            movementHandler.areCoordinatesEqual(lastMove, intArrayOf(0, -1)) -> callingPage.resources.getString(R.string.move_right_string)
            movementHandler.areCoordinatesEqual(lastMove, intArrayOf(-1, 0)) -> callingPage.resources.getString(R.string.move_down_string)
            else -> error("Next move not found")
        }
    }

    private fun getNextMove(): String =
        getCurrentLevel().bestMoves.getOrNull(movementHandler.getHistorySize() - 1)?.let { move ->
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
            if (movementHandler.isOnGoodPath(getCurrentLevel())) {
                if (movementHandler.getHistorySize() == 1) {
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
        if (movementHandler.getHistorySize() == 1) { // could remove if as already in for
            callingPage.setEquation("")
            callingPage.setCurrentScore("1")
        } else {
            var currentEquation = "1"

            var currentOperation: String

            for (i in 0 until movementHandler.getHistorySize()) {
                currentOperation = getCurrentLevel().operations[movementHandler.getCoordinateAtPosition(i)[0]][movementHandler.getCoordinateAtPosition(i)[1]].asString

                currentEquation = when (i) {
                    0 -> "1"
                    1 -> "$currentEquation$currentOperation"
                    else -> "($currentEquation)$currentOperation"
                }
            }
            callingPage.setEquation("$currentEquation\n=")
            callingPage.setCurrentScore(getFormattedScore(getCurrentScore()))
        }
    }
}

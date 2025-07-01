package com.slykos.bokoa.models

import android.annotation.SuppressLint
import com.slykos.bokoa.R
import com.slykos.bokoa.pagesHandler.TutorialPageHandler

class TutorialGame(
    private var callingPage: TutorialPageHandler
) :
    Game(
        callingPage
    ) {

    init {
        callingPage.setMaxScore("50")
    }

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
        // go trough history
        var correctUntilNow = true
        var lastMove: IntArray

        if (history.size - 1 > currentLevel.bestMoves.size) { // Todo +1 -1 ?
            correctUntilNow = false
        } else {
            for (i in 1 until history.size) {
                lastMove = intArrayOf(
                    history[i][0] - history[i - 1][0],
                    history[i][1] - history[i - 1][1]
                )

                // stop as soon as difference
                if (!isMoveInDirection(
                        currentLevel.bestMoves[i - 1],
                        lastMove
                    )
                ) {
                    correctUntilNow = false
                }
            }
        }
        return correctUntilNow
    }

    private fun getOppositeOfPreviousMove(): String {
        // TODO refactor this function

        val lastMove = intArrayOf(
            history[history.size - 2][0] - history[history.size - 1][0],
            history[history.size - 2][1] - history[history.size - 1][1]
        )

        return when {
            areCoordinatesEqual(
                lastMove,
                intArrayOf(-1, 0)
            ) -> callingPage.resources.getString(R.string.move_up)

            areCoordinatesEqual(
                lastMove,
                intArrayOf(0, -1)
            ) -> callingPage.resources.getString(R.string.move_le)

            areCoordinatesEqual(
                lastMove,
                intArrayOf(0, 1)
            ) -> callingPage.resources.getString(R.string.move_ri)

            areCoordinatesEqual(
                lastMove,
                intArrayOf(1, 0)
            ) -> callingPage.resources.getString(R.string.move_dn)

            else -> "ERROR 98"
        }
    }

    private fun getNextMove(): String =
        currentLevel.bestMoves.getOrNull(history.size - 1)?.let {
                move ->
            when (move) {
                "u" -> callingPage.resources.getString(R.string.move_dn)
                "n" -> callingPage.resources.getString(R.string.move_up)
                ">" -> callingPage.resources.getString(R.string.move_ri)
                "<" -> callingPage.resources.getString(R.string.move_le)
                else -> "ERROR 409"
            }
        } ?: ""

    private fun setTipGiver() {
        callingPage.setTip(
            if (isOnGoodPath()) {
                if (history.size == 1) {
                    callingPage.resources.getString(R.string.swipe) + getNextMove()
                } else {
                    callingPage.resources.getString(R.string.good_swipe) + getNextMove()
                }
            } else {
                callingPage.resources.getString(R.string.bad_swipe) + getOppositeOfPreviousMove()
            }
        )
    }

    @SuppressLint("SetTextI18n")
    private fun setEquationAndScoreViewer() {
        if (history.size == 1) { // could remove if as already in for
            callingPage.setEquation("")
            callingPage.setCurrentScore("1")
        } else {
            var currentEquation = "1"

            var currentOperation: String

            for (i in history.indices) {
                currentOperation = currentLevel.operations[history[i][0]][history[i][1]]

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

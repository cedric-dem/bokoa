package com.slykos.bokoa.models.game

import android.annotation.SuppressLint
import android.content.res.ColorStateList
import android.graphics.Typeface
import android.view.MotionEvent
import android.view.View
import android.view.View.OnTouchListener
import androidx.core.content.ContextCompat
import com.slykos.bokoa.R
import com.slykos.bokoa.R.color
import com.slykos.bokoa.models.viewers.GridViewer
import com.slykos.bokoa.models.Level
import com.slykos.bokoa.models.MoveResult
import com.slykos.bokoa.pagesHandler.GenericPlayPage
import java.text.DecimalFormat
import kotlin.math.abs
import kotlin.math.min
import kotlin.math.roundToInt

abstract class Game(
    private val context: GenericPlayPage
) {

    private var decimalFormat: DecimalFormat = DecimalFormat("###,###,###,##0.##")

    private lateinit var gridViewer: GridViewer;

    var history: MutableList<IntArray> = mutableListOf()
    var currentScore: Float = 0f
    private var bestScore: Float = 0f

    private lateinit var gridSize: IntArray
    private var caseSize: Int = 0
    private var textSize: Float = 0f

    lateinit var bestScoreStr: String
    private lateinit var operations: Array<Array<String>>
    lateinit var currentLevel: Level

    private var screenDimensions: IntArray
    private var marginSize: Int //todo remove that argument
    private var expectedMarginSize: Int

    private var mediumColor: ColorStateList

    private var mainTypeface: Typeface

    init {

        context.getMainView().setOnTouchListener(getTouchListener())

        screenDimensions = context.getScreenDimensions()

        marginSize = 0;
        expectedMarginSize = 3 * screenDimensions[0] / 154;

        mainTypeface = context.resources.getFont(R.font.main_font)

        mediumColor = ColorStateList.valueOf(ContextCompat.getColor(context, color.medium_color))
    }

    fun getFormattedScore(score: Float): String =
        decimalFormat.format(score.toDouble()).replace(",".toRegex(), ".")

    fun initLevel(callerGridSize: IntArray, callerCurrentLevel: Level) {
        gridSize = callerGridSize

        currentLevel = callerCurrentLevel

        // TODO isolate *k and pout in var, saves time in change level
        caseSize = min(
            ((screenDimensions[0] * 0.7) / gridSize[0]),
            ((screenDimensions[1] * 0.48) / gridSize[1])
        ).roundToInt()

        textSize = ((caseSize / 5) + 6.5).toFloat()

        operations = currentLevel.operations
        bestScore = currentLevel.bestScore
        bestScoreStr = getFormattedScore(bestScore)
    }

    fun shapeGrid() {
        this.gridViewer.shapeGrid()
    }

    fun emptyGrid() {
        this.gridViewer.emptyGrid()
    }

    fun initGame() {
        currentScore = 1f
        history = mutableListOf(intArrayOf(0, 0))
    }

    private fun createGrid() {
        gridViewer = GridViewer(this.context, gridSize, operations, mainTypeface, mediumColor, marginSize, caseSize)
    }

    fun runGame() {
        // TODO remove old grid if existing ?

        initGame()

        createGrid()

        refreshScore()
    }

    open fun refreshScore() {
        // refresh progress bar, common to both scenarios
        context.refreshProgressBar((100 * currentScore / bestScore).toInt())
    }

    private fun getTouchListener(): OnTouchListener =
        object : OnTouchListener {
            lateinit var startPosition: IntArray
            lateinit var endPosition: IntArray

            @SuppressLint("ClickableViewAccessibility")
            override fun onTouch(v: View, event: MotionEvent): Boolean {
                when (event.action) {
                    MotionEvent.ACTION_DOWN ->
                        startPosition =
                            intArrayOf(event.x.toInt(), event.y.toInt())

                    MotionEvent.ACTION_UP -> {
                        endPosition =
                            intArrayOf(event.x.toInt(), event.y.toInt())
                        executeMovement(startPosition, endPosition)
                    }
                }
                return true
            }
        }

    fun moveLeft() {
        detectCaseAndMove(intArrayOf(0, -1))
    }

    fun moveRight() {
        detectCaseAndMove(intArrayOf(0, 1))
    }

    fun moveUp() {
        detectCaseAndMove(intArrayOf(-1, 0))
    }

    fun moveDown() {
        detectCaseAndMove(intArrayOf(1, 0))
    }

    private fun executeMovement(startPosition: IntArray, endPosition: IntArray) {
        val delta = intArrayOf(
            abs(startPosition[0] - endPosition[0]),
            abs(startPosition[1] - endPosition[1])
        )

        // TODO move threshold, verify not different h l
        if (delta[0] >= delta[1] && delta[0] > 100) { // horizontal move and sufficient

            if (startPosition[0] > endPosition[0]) { // left move
                moveLeft()
            } else { // right move
                moveRight()
            }
        } else if (delta[1] > delta[0] && delta[1] > 100) { // vertical move and sufficient

            if (startPosition[1] > endPosition[1]) { // top move
                moveUp()
            } else { // bot move
                moveDown()
            }
        }
    }

    fun applyMove(move: String) {
        detectCaseAndMove(
            when (move) {
                "u" -> intArrayOf(1, 0)
                "n" -> intArrayOf(-1, 0)
                "<" -> intArrayOf(0, -1)
                ">" -> intArrayOf(0, 1)
                else -> intArrayOf(0, 0)
            }
        )
    }

    private fun applyOperation(newOperation: String, reverse: Boolean) {
        val operand: Float = Character.getNumericValue(newOperation[1]).toFloat()
        when (newOperation[0]) {
            '+' -> currentScore += if (reverse) -operand else operand
            '-' -> currentScore += if (reverse) operand else -operand
            '×' -> currentScore *= if (reverse) 1 / operand else operand
            '÷' -> currentScore *= if (reverse) operand else 1 / operand
            else -> {}
        }
    }

    internal fun areCoordinatesEqual(coordinatesA: IntArray, coordinatesB: IntArray): Boolean =
        (coordinatesA[0] == coordinatesB[0] && coordinatesA[1] == coordinatesB[1])

    private fun isOutsideBounds(newCoordinate: IntArray): Boolean =
        (newCoordinate[0] < 0 || newCoordinate[0] >= gridSize[1] || newCoordinate[1] < 0 || newCoordinate[1] >= gridSize[0])

    private fun isMoveComingBack(newCoordinate: IntArray): Boolean =
        history.size >= 2 && areCoordinatesEqual(
            history[history.size - 2],
            newCoordinate
        )

    private fun isCollidingWithPreviousCase(newCoordinate: IntArray): Boolean {
        for (i in history.indices) {
            if (areCoordinatesEqual(history[i], newCoordinate)) {
                return true
            }
        }
        return false
    }

    private fun detectSituation(newCoordinate: IntArray): MoveResult =
        when {
            isOutsideBounds(newCoordinate) -> MoveResult.IMPOSSIBLE // outside bounds, not possible
            isMoveComingBack(newCoordinate) -> MoveResult.COME_BACK // coming back one step
            isCollidingWithPreviousCase(newCoordinate) -> MoveResult.IMPOSSIBLE // coming back more than one step, not possible
            else -> MoveResult.NORMAL // normal move
        }

    private fun detectCaseAndMove(direction: IntArray) {
        // get old and new coordinates
        val oldCoordinate = history[history.size - 1]
        val newCoordinate = intArrayOf(oldCoordinate[0] + direction[0], oldCoordinate[1] + direction[1])

        // detecting_case
        val situation = detectSituation(newCoordinate)

        if (situation != MoveResult.IMPOSSIBLE) { // Move
            applyMoveResult(situation, oldCoordinate, newCoordinate)
        }
        // else no move
    }

    private fun applyMoveResult(situation: MoveResult, oldCoordinate: IntArray, newCoordinate: IntArray) {
        if (situation == MoveResult.NORMAL) {
            movementReachNew(newCoordinate) // go for new
        } else {
            movementGoBack(oldCoordinate, newCoordinate) // coming back
        }

        refreshScore()
        checkGoalReached()
        refreshBackground()
    }

    private fun refreshBackground() {

        //Inside
        for (i in 1 until history.size - 1) { // start from first non neutral, until head
            gridViewer.getCase(history[i][0], history[i][1]).shapeSnakeCase(gridViewer.detectTwoMargins(history[i - 1], history[i], history[i + 1]), ((255 * i) / history.size))
        }

        //Head + neutral
        if (history.size > 1) {
            // Neutral
            gridViewer.getCase(history[0][0], history[0][1]).shapeNeutralCase(gridViewer.detectSingleMargin(history[0], history[1]))

            // HEAD
            gridViewer.getCase(history[history.size - 1][0], history[history.size - 1][1]).shapeHeadCase(gridViewer.detectSingleMargin(history[history.size - 1], history[history.size - 2]))

        } else { //if size 0, shape neutral
            gridViewer.getCase(history[0][0], history[0][1]).shapeNeutralCaseNeverMoved()
        }
    }

    private fun checkGoalReached() {
        if (abs((currentScore - bestScore).toDouble()) <= 0.02f || currentScore > bestScore) {
            context.updateProgressBarTint(true)
            context.finishedGame()
        } else {
            context.updateProgressBarTint(false)
        }
    }

    private fun movementGoBack(oldCord: IntArray, newCord: IntArray) {
        // apply reverse operation
        applyOperation(operations[oldCord[0]][oldCord[1]], true)

        history.removeAt(history.lastIndex)

        // reset case background
        gridViewer.getCase(oldCord[0], oldCord[1]).shapeUnusedCase()

        // else if
        if (areCoordinatesEqual(intArrayOf(0, 0), newCord)) {
            currentScore = 1.0f
        }
    }

    private fun movementReachNew(newCord: IntArray) {
        // append new coordinates to snake
        history.add(newCord)

        // modify score
        applyOperation(operations[newCord[0]][newCord[1]], false)
    }
}

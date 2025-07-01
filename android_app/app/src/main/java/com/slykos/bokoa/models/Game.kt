package com.slykos.bokoa.models

import android.annotation.SuppressLint
import android.content.res.ColorStateList
import android.graphics.Typeface
import android.util.TypedValue
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.View.OnTouchListener
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.gridlayout.widget.GridLayout
import com.slykos.bokoa.R
import com.slykos.bokoa.R.color
import com.slykos.bokoa.pagesHandler.GenericPlayPage
import java.text.DecimalFormat
import kotlin.math.abs
import kotlin.math.min
import kotlin.math.roundToInt

abstract class Game(
    private val context: GenericPlayPage
) {
    private var decimalFormat: DecimalFormat = DecimalFormat("###,###,###,##0.##")

    private lateinit var operationsView: Array<Array<TextView?>>

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
    private var marginSize: Int

    private var mediumColor: ColorStateList

    private var mainTypeface: Typeface

    init {
        context.getMainView().setOnTouchListener(getTouchListener())

        screenDimensions = context.getScreenDimensions()

        marginSize = screenDimensions[0] / 154

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

    fun emptyGrid() {
        for (i in 0 until gridSize[1]) {
            for (j in 0 until gridSize[0]) {
                context.getGameGrid().removeView(operationsView[i][j])
            }
        }
    }

    fun initGame() {
        currentScore = 1f

        history = mutableListOf(intArrayOf(0, 0))
    }

    private fun createGrid() {
        operationsView = Array(gridSize[1]) {
            arrayOfNulls(
                gridSize[0]
            )
        }

        for (i in 0 until gridSize[1]) {
            for (j in 0 until gridSize[0]) {
                operationsView[i][j] = getCase(i, j, operations[i][j])

                context.getGameGrid().addView(operationsView[i][j], getGridParams(i, j))
            }
        }
    }

    private fun getCase(i: Int, j: Int, thisOp: String): TextView {
        val newCase = TextView(context.getGameGrid().context).apply {
            id = 1000 + (i * gridSize[0] + j)
            gravity = Gravity.CENTER
            setTextColor(getColorOfOperation(thisOp[0]))
            text = thisOp
            typeface = mainTypeface
        }
        newCase.setTextSize(TypedValue.COMPLEX_UNIT_SP, textSize)
        return newCase
    }
    private fun getColorOfOperation(operation: Char): Int =
        when (operation) {
            '+' -> ContextCompat.getColor(context, color.plus_color)
            '-' -> ContextCompat.getColor(context, color.minus_color)
            '×' -> ContextCompat.getColor(context, color.mul_color)
            '÷' -> ContextCompat.getColor(context, color.div_color)
            else -> ContextCompat.getColor(context, color.light_color)
        }

    private fun getGridParams(i: Int, j: Int): GridLayout.LayoutParams =
        GridLayout.LayoutParams().apply {
            setMargins(marginSize, marginSize, marginSize, marginSize)
            width = caseSize
            height = caseSize
            rowSpec = GridLayout.spec(i)
            columnSpec = GridLayout.spec(j)
        }

    fun shapeGrid() {
        for (i in 0 until gridSize[1]) {
            for (j in 0 until gridSize[0]) {
                if (operations[i][j] == "1") {
                    operationsView[i][j]!!.setBackgroundResource(R.drawable.bg_case_neutral)
                } else {
                    operationsView[i][j]!!.setBackgroundResource(R.drawable.bg_case)
                    operationsView[i][j]!!.backgroundTintList = mediumColor
                }
            }
        }
    }

    fun runGame() {
        // TODO remove old grid if existing ?

        initGame()

        createGrid()
        shapeGrid()

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

    private fun executeMovement(startPosition: IntArray, endPosition: IntArray) {
        val delta = intArrayOf(
            abs(startPosition[0] - endPosition[0]),
            abs(startPosition[1] - endPosition[1])
        )

        // TODO move threshold, verify not different h l
        if (delta[0] >= delta[1] && delta[0] > 100) { // horizontal move and sufficient

            if (startPosition[0] > endPosition[0]) { // left move
                detectCaseAndMove(intArrayOf(0, -1))
            } else { // right move
                detectCaseAndMove(intArrayOf(0, 1))
            }
        } else if (delta[1] > delta[0] && delta[1] > 100) { // vertical move and sufficient

            if (startPosition[1] > endPosition[1]) { // top move
                detectCaseAndMove(intArrayOf(-1, 0))
            } else { // bot move
                detectCaseAndMove(intArrayOf(1, 0))
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

    private fun detectCase(newCoordinate: IntArray): MoveResult =
        if (isOutsideBounds(newCoordinate)) { // Move outside bounds
            MoveResult.IMPOSSIBLE
        } else if (isMoveComingBack(newCoordinate)) { // coming back on snake
            MoveResult.COME_BACK
        } else if (isCollidingWithPreviousCase(newCoordinate)) { // new coordinates
            MoveResult.IMPOSSIBLE
        } else { // everything ok
            MoveResult.NORMAL
        }

    private fun getBlueShade(intensity: Int): Int = // intensity between 0 and 255
        (intensity and 0xff) shl 24 or (0xff)

    private fun detectCaseAndMove(direction: IntArray) {
        // get old and new coordinates
        val oldCoordinate = history[history.size - 1]
        val newCoordinate = intArrayOf(oldCoordinate[0] + direction[0], oldCoordinate[1] + direction[1])

        // detecting_case
        val situation = detectCase(newCoordinate)

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
        for (i in 1 until history.size - 1) { // start from first non neutral, until head
            changeBackgroundOfCase(history[i], CaseState.SNAKE, i) // body snake
        }
        if (history.size > 1) {
            changeBackgroundOfCase(history[history.size - 1], CaseState.HEAD, history.size - 1) // head
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
        changeBackgroundOfCase(oldCord, CaseState.SIMPLE_CASE, 0)

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

    private fun changeBackgroundOfCase(
        coordinates: IntArray,
        caseState: CaseState,
        currentIndex: Int
    ) { // Todo can remove some of them if pass "origin state" parameter
        val currentCase = operationsView[coordinates[0]][coordinates[1]]

        when (caseState) {
            CaseState.SIMPLE_CASE -> { // simple case 0
                currentCase!!.setBackgroundResource(R.drawable.bg_case)
                currentCase.backgroundTintList = mediumColor
            }
            CaseState.SNAKE -> { // snake 1
                currentCase!!.setBackgroundResource(R.drawable.bg_case)
                currentCase.backgroundTintList =
                    ColorStateList.valueOf(getBlueShade(((255 * currentIndex) / history.size)))
            }
            CaseState.HEAD -> { // head 2
                currentCase!!.setBackgroundResource(R.drawable.bg_case_head)
                currentCase.backgroundTintList = ColorStateList.valueOf(getBlueShade(255))
            }
        }
    }
}

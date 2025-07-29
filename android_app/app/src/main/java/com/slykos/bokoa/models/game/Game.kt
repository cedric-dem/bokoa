package com.slykos.bokoa.models.game

import android.content.res.ColorStateList
import android.graphics.Typeface
import android.view.MotionEvent
import android.view.View
import android.view.View.OnTouchListener
import androidx.core.content.ContextCompat
import com.slykos.bokoa.Config
import com.slykos.bokoa.R
import com.slykos.bokoa.R.color
import com.slykos.bokoa.models.GridHandler
import com.slykos.bokoa.models.Level
import com.slykos.bokoa.models.MoveResult
import com.slykos.bokoa.pagesHandler.playPages.GenericPlayPage
import java.text.DecimalFormat
import kotlin.math.abs
import kotlin.math.min
import kotlin.math.roundToInt

abstract class Game(
    private val context: GenericPlayPage
) {
    private var decimalFormat: DecimalFormat = DecimalFormat("###,###,###,##0.##")

    var coordinatesHistory: MutableList<IntArray> = mutableListOf()
    var currentScore: Float = 0f
    private var maxScore: Float = 0f

    private lateinit var gridSize: IntArray
    private var caseSize: Int = 0
    private var caseTextSize: Float = 0f

    lateinit var bestScoreString: String
    lateinit var currentLevel: Level

    private var screenDimensions: IntArray
    private var mediumColor: ColorStateList

    private var mainTypeface: Typeface
    private lateinit var gridHandler: GridHandler

    init {
        context.getMainView().setOnTouchListener(getTouchListener())

        screenDimensions = context.getScreenDimensions()

        mainTypeface = context.resources.getFont(R.font.main_font)

        mediumColor = ColorStateList.valueOf(ContextCompat.getColor(context, color.medium_color))
    }

    fun getFormattedScore(score: Float): String =
        decimalFormat.format(score.toDouble()).replace(",".toRegex(), ".")

    fun initLevel(callerGridSize: IntArray, callerCurrentLevel: Level) {
        gridSize = callerGridSize

        currentLevel = callerCurrentLevel

        // TODO isolate k ?
        caseSize = min(
            ((screenDimensions[0] * 0.7) / gridSize[0]),
            ((screenDimensions[1] * 0.48) / gridSize[1])
        ).roundToInt()

        caseTextSize = ((caseSize.toFloat() / 3.5) + -9.7).toFloat()

        this.gridHandler = GridHandler(this.context, currentLevel.operations, this.gridSize, mainTypeface, mediumColor, caseSize, caseTextSize)

        maxScore = currentLevel.bestScore
        bestScoreString = getFormattedScore(maxScore)
    }

    fun shapeGrid() {
        this.gridHandler.shapeGrid()
    }

    fun emptyGrid() {
        this.gridHandler.emptyGrid()
    }

    fun initGame() {
        currentScore = 1f
        coordinatesHistory = mutableListOf(intArrayOf(0, 0))
    }

    private fun createGrid() {
        gridHandler.createGrid()
    }

    fun runGame() {
        // TODO remove old grid if existing

        initGame()

        createGrid()

        refreshScore()
    }

    open fun refreshScore() {
        // refresh progress bar, common to both scenarios
        context.refreshProgressBar((100 * currentScore / maxScore).toInt())
    }

    private fun getTouchListener(): OnTouchListener =
        object : OnTouchListener {
            lateinit var startPosition: IntArray
            lateinit var endPosition: IntArray

            override fun onTouch(v: View, event: MotionEvent): Boolean {
                when (event.action) {
                    MotionEvent.ACTION_DOWN ->
                        startPosition = intArrayOf(event.x.toInt(), event.y.toInt())

                    MotionEvent.ACTION_UP -> {
                        endPosition = intArrayOf(event.x.toInt(), event.y.toInt())
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
        val dx = endPosition[0] - startPosition[0]
        val dy = endPosition[1] - startPosition[1]

        val absDx = abs(dx)
        val absDy = abs(dy)

        // TODO verify threshold not different h l
        when {
            absDx >= absDy && absDx > Config.MOVE_THRESHOLD -> { // move horizontal
                if (dx > 0) moveRight() else moveLeft()
            }

            absDy > absDx && absDy > Config.MOVE_THRESHOLD -> { // move vertical
                if (dy > 0) moveDown() else moveUp()
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
        coordinatesHistory.size >= 2 && areCoordinatesEqual(
            coordinatesHistory[coordinatesHistory.size - 2],
            newCoordinate
        )

    private fun isCollidingWithPreviousCase(newCoordinate: IntArray): Boolean =
        coordinatesHistory.any { areCoordinatesEqual(it, newCoordinate) }

    private fun detectSituation(newCoordinate: IntArray): MoveResult =
        when {
            isOutsideBounds(newCoordinate) -> MoveResult.IMPOSSIBLE // outside bounds, not possible
            isMoveComingBack(newCoordinate) -> MoveResult.COME_BACK // coming back one step
            isCollidingWithPreviousCase(newCoordinate) -> MoveResult.IMPOSSIBLE // coming back more than one step, not possible
            else -> MoveResult.NORMAL // normal move
        }

    private fun detectCaseAndMove(direction: IntArray) {
        val oldCoordinate = coordinatesHistory.last()
        val newCoordinate = intArrayOf(oldCoordinate[0] + direction[0], oldCoordinate[1] + direction[1])

        detectSituation(newCoordinate)
            .takeIf { it != MoveResult.IMPOSSIBLE }
            ?.let { applyMoveResult(it, oldCoordinate, newCoordinate) }
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

    private fun refreshBackground() { //todo move lot of computation in gridhandler

        // Inside
        for (i in 1 until coordinatesHistory.size - 1) { // start from first non neutral, until cursor
            gridHandler.getCase(coordinatesHistory[i]).shapeInHistoryCase(gridHandler.detectTwoMargins(coordinatesHistory[i - 1], coordinatesHistory[i], coordinatesHistory[i + 1]), ((255 * i) / coordinatesHistory.size))
        }

        if (coordinatesHistory.size > 1) { // cursor + neutral if more than one elem
            // Neutral
            gridHandler.getCase(coordinatesHistory[0]).shapeNeutralCase(gridHandler.detectSingleMargin(coordinatesHistory[0], coordinatesHistory[1]))

            // cursor
            gridHandler.getCase(coordinatesHistory.last()).shapeCursorCase(gridHandler.detectSingleMargin(coordinatesHistory.last(), coordinatesHistory[coordinatesHistory.size - 2]))

        } else { //if size 0, shape neutral only
            gridHandler.getCase(coordinatesHistory[0]).shapeNeutralCaseNeverMoved()
        }
    }

    private fun checkGoalReached() {
        if (abs((currentScore - maxScore).toDouble()) <= 0.02f || currentScore > maxScore) {
            context.updateProgressBarTint(true)
            context.finishedGame()
        } else {
            context.updateProgressBarTint(false)
        }
    }

    private fun movementGoBack(oldCord: IntArray, newCord: IntArray) {
        // apply reverse operation
        applyOperation(gridHandler.getOperation(oldCord), true)

        coordinatesHistory.removeAt(coordinatesHistory.lastIndex)

        // reset  old case background
        gridHandler.getCase(oldCord).shapeUnusedCase()

        if (areCoordinatesEqual(intArrayOf(0, 0), newCord)) {
            currentScore = 1.0f
        }
    }

    private fun movementReachNew(newCord: IntArray) {
        // append new coordinates to history
        coordinatesHistory.add(newCord)

        // modify score
        applyOperation(gridHandler.getOperation(newCord), false)
    }
}

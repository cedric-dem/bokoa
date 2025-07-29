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
import com.slykos.bokoa.models.MovementHandler
import com.slykos.bokoa.pagesHandler.playPages.GenericPlayPage
import java.text.DecimalFormat
import kotlin.math.abs

abstract class Game(
    private val context: GenericPlayPage
) {
    private var decimalFormat: DecimalFormat = DecimalFormat("###,###,###,##0.##")

    var currentScore: Float = 0f
    private var maxScore: Float = 0f

    lateinit var bestScoreString: String
    lateinit var currentLevel: Level

    private lateinit var gridHandler: GridHandler
    protected lateinit var movementHandler: MovementHandler

    init {
        context.getMainView().setOnTouchListener(getTouchListener())
    }

    fun getFormattedScore(score: Float): String =
        decimalFormat.format(score.toDouble()).replace(",".toRegex(), ".")

    fun initLevel(callerGridSize: IntArray, callerCurrentLevel: Level) {

        currentLevel = callerCurrentLevel

        // TODO isolate k ?
        movementHandler = MovementHandler(callerGridSize, this)

        gridHandler = GridHandler(this.context, currentLevel.operations, callerGridSize, context.resources.getFont(R.font.main_font), ColorStateList.valueOf(ContextCompat.getColor(context, color.medium_color)), context.getScreenDimensions())

        maxScore = currentLevel.bestScore
        bestScoreString = getFormattedScore(maxScore)
    }

    fun shapeGrid() {
        gridHandler.shapeGrid()
    }

    fun emptyGrid() {
        gridHandler.emptyGrid()
    }

    fun initGame() {
        movementHandler.start()
        currentScore = 1f
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
        movementHandler.detectCaseAndMove(intArrayOf(0, -1))
    }

    fun moveRight() {
        movementHandler.detectCaseAndMove(intArrayOf(0, 1))
    }

    fun moveUp() {
        movementHandler.detectCaseAndMove(intArrayOf(-1, 0))
    }

    fun moveDown() {
        movementHandler.detectCaseAndMove(intArrayOf(1, 0))
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

    fun refreshScoreVisual() {
        refreshScore()
        checkGoalReached()
        gridHandler.refreshBackground(movementHandler.getEntireHistory())
    }

    fun applyMove(move: String) {
        movementHandler.detectCaseAndMove(
            when (move) {
                "u" -> intArrayOf(1, 0)
                "n" -> intArrayOf(-1, 0)
                "<" -> intArrayOf(0, -1)
                ">" -> intArrayOf(0, 1)
                else -> intArrayOf(0, 0)
            }
        )
    }

    fun applyOperationOnScore(oldCord: IntArray, newCord: IntArray) {
        // apply reverse operation
        applyOperation(gridHandler.getOperation(oldCord), true)
    }

    fun gameMovementGoBack(oldCord: IntArray, newCord: IntArray) {
        // reset  old case background
        gridHandler.getCase(oldCord).shapeUnusedCase()

        if (movementHandler.areCoordinatesEqual(intArrayOf(0, 0), newCord)) {
            currentScore = 1.0f
        }
    }

    fun movementReachNew(newCord: IntArray) {
        // modify score
        applyOperation(gridHandler.getOperation(newCord), false)
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

    private fun checkGoalReached() {
        if (abs((currentScore - maxScore).toDouble()) <= 0.02f || currentScore > maxScore) {
            context.updateProgressBarTint(true)
            context.finishedGame()
        } else {
            context.updateProgressBarTint(false)
        }
    }
}

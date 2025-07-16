package com.slykos.bokoa.models

import android.annotation.SuppressLint
import android.content.res.ColorStateList
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.util.TypedValue
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.View.OnTouchListener
import android.view.ViewGroup
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
    private var blueBias = 80
    private val centerWeight = 0.8f
    private val oneCornerRadius = 50f
    private val twoCornerRadius = 50f

    private var decimalFormat: DecimalFormat = DecimalFormat("###,###,###,##0.##")

    private lateinit var operationsView: Array<Array<GridLayout ?>>

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
        expectedMarginSize = 3*  screenDimensions[0] / 154;

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

        this.shapeGrid()
    }

    private fun getCase(i: Int, j: Int, thisOp: String): GridLayout {

        val context = context.getGameGrid().context

        val gridLayout = GridLayout(context).apply {
            rowCount = 3
            columnCount = 3
            layoutParams = ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT
            )
        }

        val sideWeight = (1f - centerWeight) / 2f

        val rowWeights = floatArrayOf(sideWeight, centerWeight, sideWeight)
        val colWeights = floatArrayOf(sideWeight, centerWeight, sideWeight)

        for (row in 0 until 3) {
            for (col in 0 until 3) {
                val isCenter = row == 1 && col == 1

                val view: View = if (isCenter) {
                    TextView(context).apply {
                        id = 1000 + (i * gridSize[0] + j)
                        gravity = Gravity.CENTER
                        text = thisOp
                        setTextColor(getColorOfOperation(thisOp[0]))
                        typeface = mainTypeface
                        setPadding(0, 0, 0, 0)
                        setTextSize(TypedValue.COMPLEX_UNIT_SP, textSize)
                        layoutParams = GridLayout.LayoutParams().apply {
                            width = 0
                            height = 0
                            rowSpec = GridLayout.spec(row, rowWeights[row])
                            columnSpec = GridLayout.spec(col, colWeights[col])
                        }
                    }
                } else {
                    View(context).apply {
                        backgroundTintList = ColorStateList.valueOf(ContextCompat.getColor(context, color.dark_color))
                        layoutParams = GridLayout.LayoutParams().apply {
                            width = 0
                            height = 0
                            rowSpec = GridLayout.spec(row, rowWeights[row])
                            columnSpec = GridLayout.spec(col, colWeights[col])
                        }
                    }
                }

                gridLayout.addView(view)
            }
        }
        return gridLayout
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
                    shapeNeutralCaseNeverMoved(operationsView[i][j]!!)
                } else {
                    shapeUnusedCase(operationsView[i][j]!!)
                }
            }
        }
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

    fun moveLeft(){
        detectCaseAndMove(intArrayOf(0, -1))
    }

    fun moveRight(){
        detectCaseAndMove(intArrayOf(0, 1))
    }

    fun moveUp(){
        detectCaseAndMove(intArrayOf(-1, 0))
    }

    fun moveDown(){
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

    private fun detectCaseAndMove(direction: IntArray) {
        // get old and new coordinates
        val oldCoordinate = history[history.size - 1]
        val newCoordinate =
            intArrayOf(oldCoordinate[0] + direction[0], oldCoordinate[1] + direction[1])

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

        //Inside
        for (i in  1 until history.size - 1) { // start from first non neutral, until head

            shapeSnakeCase(
                operationsView[history[i][0]][history[i][1]]!!,
                detectTwoMargins(history[i-1], history[i], history[i+1]),
                ((255 * i) / history.size)
            )
        }

        //Head + neutral
        if (history.size > 1) {
            ////////////////////////////////////////////////////////////////////////////////////////////// Neutral
            shapeNeutralCase(
                operationsView[history[0][0]][history[0][1]]!!,
                detectSingleMargin(history[0], history[1])
            )

            ////////////////////////////////////////////////////////////////////////////////////////////// HEAD
            shapeHeadCase(
                operationsView[history[history.size - 1][0]][history[history.size - 1][1]]!!,
                detectSingleMargin(history[history.size - 1], history[history.size - 2])
            )

        } else { //if size 0, shape neutral
            shapeNeutralCaseNeverMoved(
                operationsView[history[0][0]][history[0][1]]!!
            )

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

        val currentCase = operationsView[oldCord[0]][oldCord[1]]
        shapeUnusedCase(currentCase!!)

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

    private fun detectDirection(coordinatesA: IntArray, coordinatesB: IntArray): Int {
        return when {
            coordinatesA[0] == coordinatesB[0] && coordinatesA[1] > coordinatesB[1] -> 0 // left
            coordinatesA[0] == coordinatesB[0] && coordinatesA[1] < coordinatesB[1] -> 2 // right
            coordinatesA[0] > coordinatesB[0] -> 1 // up
            else -> 3 // bottom
        }
    }

    private fun detectSingleMargin(prev: IntArray, current: IntArray): BooleanArray =
        BooleanArray(4).apply {
            this[detectDirection(current, prev)] = true
        }

    private fun detectTwoMargins(prev: IntArray, current: IntArray, next: IntArray): BooleanArray =
        BooleanArray(4).apply {
            this[detectDirection(prev, current)] = true
            this[detectDirection(next, current)] = true
        }

    private fun getCornerRadiiOneSide(sides:  BooleanArray): FloatArray =
        when {
            !sides[2] && !sides[3] -> floatArrayOf( oneCornerRadius, oneCornerRadius, 0f, 0f,  0f, 0f, 0f, 0f)
            !sides[0] && !sides[3] -> floatArrayOf( 0f, 0f, oneCornerRadius, oneCornerRadius, 0f, 0f, 0f, 0f )
            !sides[0] && !sides[1] -> floatArrayOf( 0f, 0f, 0f, 0f, oneCornerRadius, oneCornerRadius, 0f, 0f)
            !sides[1] && !sides[2] -> floatArrayOf( 0f, 0f, 0f, 0f,  0f, 0f, oneCornerRadius, oneCornerRadius )
            else -> FloatArray(8)
        }

    private fun getCornerRadiiTwoSide(sides: BooleanArray): FloatArray =
        when {
            sides[0]-> floatArrayOf(twoCornerRadius, twoCornerRadius,0f, 0f, 0f, 0f,twoCornerRadius, twoCornerRadius)
            sides[1]-> floatArrayOf(twoCornerRadius, twoCornerRadius,twoCornerRadius, twoCornerRadius, 0f, 0f, 0f, 0f)
            sides[2]-> floatArrayOf(0f, 0f, twoCornerRadius, twoCornerRadius,twoCornerRadius, twoCornerRadius, 0f, 0f)
            sides[3]-> floatArrayOf(0f, 0f, 0f, 0f, twoCornerRadius, twoCornerRadius,twoCornerRadius, twoCornerRadius)
            else -> FloatArray(8)
        }

    private fun setInitialCaseBorderRadius(view: View) {
        view.background = GradientDrawable().apply {
            cornerRadii = floatArrayOf( twoCornerRadius, twoCornerRadius, twoCornerRadius, twoCornerRadius,  twoCornerRadius, twoCornerRadius, twoCornerRadius, twoCornerRadius )
        }
    }

    private fun setSingleBorderRadius(view: View, sides: BooleanArray) {
        view.background = GradientDrawable().apply {
            cornerRadii = getCornerRadiiOneSide(sides)
        }
    }

    private fun setTwoBorderRadius(currentCase: View, sides: BooleanArray) {
        currentCase.background = GradientDrawable().apply {
            cornerRadii = getCornerRadiiTwoSide(sides)
        }
    }

    private fun getBiasedBlue(intensity: Int): Int =
        (blueBias + intensity * ( (255 - blueBias).toDouble() / 255.0 )).toInt()

    private fun getBlueColorStateList(intensity: Int): ColorStateList =
        ColorStateList.valueOf(Color.argb(255, 0, 0, getBiasedBlue(intensity).coerceIn(0, 255)))

    private fun  setBlackBackgroundCase(currentCase: GridLayout){
        for (i in 0 until 9) {
            if (i!=4){
                currentCase.getChildAt(i).backgroundTintList = ColorStateList.valueOf(ContextCompat.getColor(context, color.dark_color))
                currentCase.getChildAt(i).setBackgroundResource(R.drawable.bg_case_margin)
            }
        }
    }

    private fun shapeNeutralCaseNeverMoved(currentCase: GridLayout){
        currentCase.getChildAt(4).backgroundTintList = getBlueColorStateList(255)
        setInitialCaseBorderRadius(currentCase.getChildAt(4))
        setBlackBackgroundCase(currentCase)
    }

    private fun shapeNeutralCase(currentCase: GridLayout, sides: BooleanArray){
        currentCase.getChildAt(4).backgroundTintList =  getBlueColorStateList(0)
        setTwoBorderRadius(currentCase.getChildAt(4), sides)
        colorMargins(currentCase, 0, sides)
    }

    private fun shapeUnusedCase(currentCase: GridLayout ){
        currentCase.getChildAt(4).backgroundTintList = mediumColor
        currentCase.getChildAt(4).setBackgroundResource(R.drawable.bg_case)
        setBlackBackgroundCase(currentCase)
    }

    private fun shapeHeadCase(currentCase: GridLayout, sides:BooleanArray ){
        currentCase.getChildAt(4).backgroundTintList =  getBlueColorStateList(255)
        setTwoBorderRadius(currentCase.getChildAt(4), sides)
        colorMargins(currentCase, 255, sides)
    }

    private fun shapeSnakeCase(currentCase: GridLayout, sides: BooleanArray, intensity: Int) {
        currentCase.getChildAt(4).backgroundTintList =  getBlueColorStateList(intensity)
        setSingleBorderRadius(currentCase.getChildAt(4), sides)
        colorMargins(currentCase, intensity, sides)
    }

    private fun colorMargins(currentCase: GridLayout, intensity: Int, sides:  BooleanArray){
        colorMarginAtCondition(sides[0], 5, currentCase, intensity)
        colorMarginAtCondition(sides[1], 7, currentCase, intensity)
        colorMarginAtCondition(sides[2], 3, currentCase, intensity)
        colorMarginAtCondition(sides[3], 1, currentCase, intensity)
    }

    private fun colorMarginAtCondition(condition: Boolean, caseIndex: Int, currentCase: GridLayout, intensityIfCondition: Int){
        val color = if (condition) {
            getBlueColorStateList(intensityIfCondition)
        } else {
            ColorStateList.valueOf(ContextCompat.getColor(context, color.dark_color))
        }
        currentCase.getChildAt(caseIndex).backgroundTintList = color
    }
}

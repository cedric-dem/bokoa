package com.slykos.bokoa.frontend.view

import android.content.res.ColorStateList
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.util.TypedValue
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.gridlayout.widget.GridLayout
import com.slykos.bokoa.config.Config
import com.slykos.bokoa.R
import com.slykos.bokoa.frontend.pages.playPages.GenericPlayPage

class CaseViewer(
    private var context: GenericPlayPage,
    columnIndex: Int,
    rowIndex: Int,
    thisOperation: String,
    gridSize: IntArray,
    mainTypeface: Typeface,
    private val mediumColor: ColorStateList,
    private val darkColor: ColorStateList,
    private val caseTextSize: Int
) {

    var caseRepresentation: GridLayout = GridLayout(context.getGameGrid().context).apply {
        rowCount = 3
        columnCount = 3
        layoutParams = ViewGroup.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.MATCH_PARENT
        )
    }

    init {
        val sideWeight = (1f - Config.CASE_CENTER_WEIGHT) / 2f

        val rowWeights = floatArrayOf(sideWeight, Config.CASE_CENTER_WEIGHT, sideWeight)
        val colWeights = floatArrayOf(sideWeight, Config.CASE_CENTER_WEIGHT, sideWeight)

        for (row in 0 until 3) {
            for (col in 0 until 3) {

                val view: View = if (row == 1 && col == 1) {
                    getCenterPartOfTheCase(columnIndex, gridSize[0], rowIndex, thisOperation, mainTypeface, row, col, rowWeights[row], colWeights[col])
                } else {
                    getOuterPartOfTheCase(row, col, rowWeights[row], colWeights[col])
                }

                caseRepresentation.addView(view)
            }
        }
    }

    private fun getOuterPartOfTheCase(row: Int, column: Int, rowWeight: Float, colWeight: Float): View =
        View(context).apply {
            backgroundTintList = darkColor
            layoutParams = GridLayout.LayoutParams().apply {
                width = 0
                height = 0
                rowSpec = GridLayout.spec(row, rowWeight)
                columnSpec = GridLayout.spec(column, colWeight)
            }
        }

    private fun getCenterPartOfTheCase(rowIndex: Int, colWidth: Int, columnIndex: Int, thisOperation: String, mainTypeface: Typeface, row: Int, col: Int, rowWeight: Float, colWeight: Float): TextView =
        TextView(context).apply {
            id = 1000 + (rowIndex * colWidth + columnIndex)
            gravity = Gravity.CENTER
            text = thisOperation
            setTextColor(getColorOfOperation(thisOperation[0]))
            typeface = mainTypeface
            setPadding(0, 0, 0, 0)
            setTextSize(TypedValue.COMPLEX_UNIT_SP, caseTextSize.toFloat())
            layoutParams = GridLayout.LayoutParams().apply {
                width = 0
                height = 0
                rowSpec = GridLayout.spec(row, rowWeight)
                columnSpec = GridLayout.spec(col, colWeight)
            }
        }

    private fun getColorOfOperation(operation: Char): Int =
        when (operation) {
            '+' -> ContextCompat.getColor(context, R.color.plus_color)
            '-' -> ContextCompat.getColor(context, R.color.minus_color)
            '×' -> ContextCompat.getColor(context, R.color.mul_color)
            '÷' -> ContextCompat.getColor(context, R.color.div_color)
            else -> ContextCompat.getColor(context, R.color.light_color)
        }

    private fun getCornerRadiiOneSide(sides: BooleanArray): FloatArray =
        when {
            sides[0] && sides[1] -> floatArrayOf(Config.CORNER_RADIUS_ONE_CORNER, Config.CORNER_RADIUS_ONE_CORNER, 0f, 0f, 0f, 0f, 0f, 0f)
            sides[1] && sides[2] -> floatArrayOf(0f, 0f, Config.CORNER_RADIUS_ONE_CORNER, Config.CORNER_RADIUS_ONE_CORNER, 0f, 0f, 0f, 0f)
            sides[2] && sides[3] -> floatArrayOf(0f, 0f, 0f, 0f, Config.CORNER_RADIUS_ONE_CORNER, Config.CORNER_RADIUS_ONE_CORNER, 0f, 0f)
            sides[0] && sides[3] -> floatArrayOf(0f, 0f, 0f, 0f, 0f, 0f, Config.CORNER_RADIUS_ONE_CORNER, Config.CORNER_RADIUS_ONE_CORNER)
            else -> FloatArray(8)
        }

    private fun getCornerRadiiTwoSide(sides: BooleanArray): FloatArray =
        when {
            sides[0] -> floatArrayOf(Config.CORNER_RADIUS_TWO_CORNERS, Config.CORNER_RADIUS_TWO_CORNERS, 0f, 0f, 0f, 0f, Config.CORNER_RADIUS_TWO_CORNERS, Config.CORNER_RADIUS_TWO_CORNERS)
            sides[1] -> floatArrayOf(Config.CORNER_RADIUS_TWO_CORNERS, Config.CORNER_RADIUS_TWO_CORNERS, Config.CORNER_RADIUS_TWO_CORNERS, Config.CORNER_RADIUS_TWO_CORNERS, 0f, 0f, 0f, 0f)
            sides[2] -> floatArrayOf(0f, 0f, Config.CORNER_RADIUS_TWO_CORNERS, Config.CORNER_RADIUS_TWO_CORNERS, Config.CORNER_RADIUS_TWO_CORNERS, Config.CORNER_RADIUS_TWO_CORNERS, 0f, 0f)
            sides[3] -> floatArrayOf(0f, 0f, 0f, 0f, Config.CORNER_RADIUS_TWO_CORNERS, Config.CORNER_RADIUS_TWO_CORNERS, Config.CORNER_RADIUS_TWO_CORNERS, Config.CORNER_RADIUS_TWO_CORNERS)
            else -> FloatArray(8)
        }

    private fun getCornerRadii(sides: BooleanArray): FloatArray =
        when (sides.count { it }) {
            2 -> getCornerRadiiOneSide(sides)
            1 -> getCornerRadiiTwoSide(sides)
            else -> FloatArray(8)
        }

    private fun setMarginBorderRadius(view: View) {
        view.background = GradientDrawable().apply {
            cornerRadii = floatArrayOf(0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f)
        }
    }

    private fun setGenericCaseBorderRadius(view: View) {
        view.background = GradientDrawable().apply {
            cornerRadii = floatArrayOf(Config.CORNER_RADIUS_FOUR_CORNERS, Config.CORNER_RADIUS_FOUR_CORNERS, Config.CORNER_RADIUS_FOUR_CORNERS, Config.CORNER_RADIUS_FOUR_CORNERS, Config.CORNER_RADIUS_FOUR_CORNERS, Config.CORNER_RADIUS_FOUR_CORNERS, Config.CORNER_RADIUS_FOUR_CORNERS, Config.CORNER_RADIUS_FOUR_CORNERS)
        }
    }

    private fun setBorderRadius(view: View, sides: BooleanArray) {
        view.background = GradientDrawable().apply {
            cornerRadii = getCornerRadii(sides)
        }
    }

    private fun getBiasedBlue(intensity: Int): Int =
        (Config.BLUE_VALUE_INITIAL + intensity * ((255 - Config.BLUE_VALUE_INITIAL).toDouble() / 255.0)).toInt()

    private fun getBlueColorStateList(intensity: Int): ColorStateList = //TODO refactor handling of blue, not anymore between 0 and 255
        ColorStateList.valueOf(Color.argb(255, 0, 0, getBiasedBlue(intensity).coerceIn(0, 255)))

    private fun setBlackBackgroundCase() {
        for (i in 0 until 9) {
            if (i != 4) {
                caseRepresentation.getChildAt(i).backgroundTintList = darkColor
                setMarginBorderRadius(caseRepresentation.getChildAt(i))
            }
        }
    }

    fun shapeNeutralCaseNeverMoved() {
        this.caseRepresentation.getChildAt(4).backgroundTintList = getBlueColorStateList(255)
        setGenericCaseBorderRadius(this.caseRepresentation.getChildAt(4))
        setBlackBackgroundCase()
    }

    fun shapeNeutralCase(sides: BooleanArray) {
        this.caseRepresentation.getChildAt(4).backgroundTintList = getBlueColorStateList(0)
        setBorderRadius(this.caseRepresentation.getChildAt(4), sides)
        colorMargins(this.caseRepresentation, 0, sides)
    }

    fun shapeUnusedCase() {
        this.caseRepresentation.getChildAt(4).backgroundTintList = mediumColor
        setGenericCaseBorderRadius(this.caseRepresentation.getChildAt(4))
        setBlackBackgroundCase()
    }

    fun shapeCursorCase(sides: BooleanArray) {
        this.caseRepresentation.getChildAt(4).backgroundTintList = getBlueColorStateList(255)
        setBorderRadius(this.caseRepresentation.getChildAt(4), sides)
        colorMargins(this.caseRepresentation, 255, sides)
    }

    fun shapeInHistoryCase(sides: BooleanArray, intensity: Int) {
        this.caseRepresentation.getChildAt(4).backgroundTintList = getBlueColorStateList(intensity)
        setBorderRadius(this.caseRepresentation.getChildAt(4), sides)
        colorMargins(this.caseRepresentation, intensity, sides)
    }

    private fun colorMargins(currentCase: GridLayout, intensity: Int, sides: BooleanArray) {
        colorMarginAtCondition(sides[0], 5, currentCase, intensity)
        colorMarginAtCondition(sides[1], 7, currentCase, intensity)
        colorMarginAtCondition(sides[2], 3, currentCase, intensity)
        colorMarginAtCondition(sides[3], 1, currentCase, intensity)
    }

    private fun colorMarginAtCondition(condition: Boolean, caseIndex: Int, currentCase: GridLayout, intensityIfCondition: Int) {
        val color = if (condition) {
            getBlueColorStateList(intensityIfCondition)
        } else {
            darkColor
        }
        currentCase.getChildAt(caseIndex).backgroundTintList = color
    }
}
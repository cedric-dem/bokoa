package com.slykos.bokoa.models.viewers

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
import com.slykos.bokoa.R
import com.slykos.bokoa.pagesHandler.GenericPlayPage

class CaseViewer(
    private var context: GenericPlayPage,
    i: Int,
    j: Int,
    thisOp: String,
    gridSize: IntArray,
    mainTypeface: Typeface,
    private val mediumColor: ColorStateList,
    private val darkColor: ColorStateList
) {
    private var blueBias = 80
    private val centerWeight = 0.8f
    private val oneCornerRadius = 50f
    private val twoCornerRadius = 50f

    var caseRepresentation: GridLayout = GridLayout(context.getGameGrid().context).apply {
        rowCount = 3
        columnCount = 3
        layoutParams = ViewGroup.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.MATCH_PARENT
        )
    }

    init {
        val sideWeight = (1f - centerWeight) / 2f

        val rowWeights = floatArrayOf(sideWeight, centerWeight, sideWeight)
        val colWeights = floatArrayOf(sideWeight, centerWeight, sideWeight)

        for (row in 0 until 3) {
            for (col in 0 until 3) {

                val view: View = if (row == 1 && col == 1) {
                    getCenterPartOfTheCase(i, gridSize[0], j, thisOp, mainTypeface, row, col, rowWeights[row], colWeights[col])
                } else {
                    getOuterPartOfTheCase(row, col, rowWeights[row], colWeights[col])
                }

                caseRepresentation.addView(view)
            }
        }
    }

    private fun getOuterPartOfTheCase(row: Int, col: Int, rowWeight: Float, colWeight: Float): View =
        View(context).apply {
            backgroundTintList = darkColor
            layoutParams = GridLayout.LayoutParams().apply {
                width = 0
                height = 0
                rowSpec = GridLayout.spec(row, rowWeight)
                columnSpec = GridLayout.spec(col, colWeight)
            }
        }

    private fun getCenterPartOfTheCase(i: Int, colWidth: Int, j: Int, thisOp: String, mainTypeface: Typeface, row: Int, col: Int, rowWeight: Float, colWeight: Float): TextView =
        TextView(context).apply {
            id = 1000 + (i * colWidth + j)
            gravity = Gravity.CENTER
            text = thisOp
            setTextColor(getColorOfOperation(thisOp[0]))
            typeface = mainTypeface
            setPadding(0, 0, 0, 0)
            setTextSize(TypedValue.COMPLEX_UNIT_SP, textSize)
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
            sides[0] && sides[1] -> floatArrayOf(oneCornerRadius, oneCornerRadius, 0f, 0f, 0f, 0f, 0f, 0f)
            sides[1] && sides[2] -> floatArrayOf(0f, 0f, oneCornerRadius, oneCornerRadius, 0f, 0f, 0f, 0f)
            sides[2] && sides[3] -> floatArrayOf(0f, 0f, 0f, 0f, oneCornerRadius, oneCornerRadius, 0f, 0f)
            sides[0] && sides[3] -> floatArrayOf(0f, 0f, 0f, 0f, 0f, 0f, oneCornerRadius, oneCornerRadius)
            else -> FloatArray(8)
        }

    private fun getCornerRadiiTwoSide(sides: BooleanArray): FloatArray =
        when {
            sides[0] -> floatArrayOf(twoCornerRadius, twoCornerRadius, 0f, 0f, 0f, 0f, twoCornerRadius, twoCornerRadius)
            sides[1] -> floatArrayOf(twoCornerRadius, twoCornerRadius, twoCornerRadius, twoCornerRadius, 0f, 0f, 0f, 0f)
            sides[2] -> floatArrayOf(0f, 0f, twoCornerRadius, twoCornerRadius, twoCornerRadius, twoCornerRadius, 0f, 0f)
            sides[3] -> floatArrayOf(0f, 0f, 0f, 0f, twoCornerRadius, twoCornerRadius, twoCornerRadius, twoCornerRadius)
            else -> FloatArray(8)
        }

    private fun getCornerRadii(sides: BooleanArray): FloatArray =
        when (sides.count { it }) {
            2 -> getCornerRadiiOneSide(sides)
            1 -> getCornerRadiiTwoSide(sides)
            else -> FloatArray(8)
        }

    private fun setInitialCaseBorderRadius(view: View) {
        view.background = GradientDrawable().apply {
            cornerRadii = floatArrayOf(twoCornerRadius, twoCornerRadius, twoCornerRadius, twoCornerRadius, twoCornerRadius, twoCornerRadius, twoCornerRadius, twoCornerRadius)
        }
    }

    private fun setBorderRadius(view: View, sides: BooleanArray) {
        view.background = GradientDrawable().apply {
            cornerRadii = getCornerRadii(sides)
        }
    }

    private fun getBiasedBlue(intensity: Int): Int =
        (blueBias + intensity * ((255 - blueBias).toDouble() / 255.0)).toInt()

    private fun getBlueColorStateList(intensity: Int): ColorStateList =
        ColorStateList.valueOf(Color.argb(255, 0, 0, getBiasedBlue(intensity).coerceIn(0, 255)))

    private fun setBlackBackgroundCase() {
        for (i in 0 until 9) {
            if (i != 4) {
                caseRepresentation.getChildAt(i).backgroundTintList = darkColor
                caseRepresentation.getChildAt(i).setBackgroundResource(R.drawable.bg_case_margin)
            }
        }
    }

    fun shapeNeutralCaseNeverMoved() {
        this.caseRepresentation.getChildAt(4).backgroundTintList = getBlueColorStateList(255)
        setInitialCaseBorderRadius(this.caseRepresentation.getChildAt(4))
        setBlackBackgroundCase()
    }

    fun shapeNeutralCase(sides: BooleanArray) {
        this.caseRepresentation.getChildAt(4).backgroundTintList = getBlueColorStateList(0)
        setBorderRadius(this.caseRepresentation.getChildAt(4), sides)
        colorMargins(this.caseRepresentation, 0, sides)
    }

    fun shapeUnusedCase() {
        this.caseRepresentation.getChildAt(4).backgroundTintList = mediumColor
        this.caseRepresentation.getChildAt(4).setBackgroundResource(R.drawable.bg_case)
        setBlackBackgroundCase()
    }

    fun shapeHeadCase(sides: BooleanArray) {
        this.caseRepresentation.getChildAt(4).backgroundTintList = getBlueColorStateList(255)
        setBorderRadius(this.caseRepresentation.getChildAt(4), sides)
        colorMargins(this.caseRepresentation, 255, sides)
    }

    fun shapeSnakeCase(sides: BooleanArray, intensity: Int) {
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
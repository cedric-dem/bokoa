package com.slykos.bokoa.models.viewers

import android.content.res.ColorStateList
import android.graphics.Typeface
import android.util.Log
import androidx.core.content.ContextCompat
import androidx.gridlayout.widget.GridLayout
import com.slykos.bokoa.R
import com.slykos.bokoa.models.Operation
import com.slykos.bokoa.pagesHandler.playPages.GenericPlayPage

class GridViewer(
    private var context: GenericPlayPage,
    private val gridSize: IntArray,
    private val operationsGrid: Array<Array<Operation>>,
    mainTypeface: Typeface,
    mediumColor: ColorStateList,
    private val caseSize: Int,
    private val caseTextSize: Int
) {

    private val gridViewer: Array<Array<CaseViewer?>> = Array(gridSize[1]) { arrayOfNulls(gridSize[0]) }

    init {
        val darkColor = ColorStateList.valueOf(ContextCompat.getColor(context, R.color.dark_color))
        for (i in 0 until gridSize[1]) {
            for (j in 0 until gridSize[0]) {
                this.gridViewer[i][j] = CaseViewer(this.context, i, j, operationsGrid[i][j].asString, gridSize, mainTypeface, mediumColor, darkColor, caseTextSize)
                context.getGameGrid().addView(this.gridViewer[i][j]!!.caseRepresentation, getGridParams(i, j))
            }
        }
        this.shapeGrid()
    }

    private fun getGridParams(rowIndex: Int, columnIndex: Int): GridLayout.LayoutParams =
        GridLayout.LayoutParams().apply {
            setMargins(0, 0, 0, 0)
            width = caseSize
            height = caseSize
            rowSpec = GridLayout.spec(rowIndex)
            columnSpec = GridLayout.spec(columnIndex)
        }

    fun emptyGrid() {
        for (i in 0 until gridSize[1]) {
            for (j in 0 until gridSize[0]) {
                context.getGameGrid().removeView(this.gridViewer[i][j]!!.caseRepresentation)
            }
        }
    }

    fun shapeGrid() {
        for (i in 0 until gridSize[1]) {
            for (j in 0 until gridSize[0]) {
                if (operationsGrid[i][j].isNeutral) {
                    this.gridViewer[i][j]!!.shapeNeutralCaseNeverMoved()
                } else {
                    this.gridViewer[i][j]!!.shapeUnusedCase()
                }
            }
        }
    }

    fun getCase(coordinates: IntArray): CaseViewer =
        this.gridViewer[coordinates[0]][coordinates[1]]!!

    // Static
    private fun detectDirection(coordinatesA: IntArray, coordinatesB: IntArray): Int {
        return when {
            coordinatesA[0] == coordinatesB[0] && coordinatesA[1] > coordinatesB[1] -> 0 // left
            coordinatesA[0] == coordinatesB[0] && coordinatesA[1] < coordinatesB[1] -> 2 // right
            coordinatesA[0] > coordinatesB[0] -> 1 // up
            else -> 3 // bottom
        }
    }

    // Static
    fun detectSingleMargin(previousCoordinates: IntArray, currentCoordinates: IntArray): BooleanArray =
        BooleanArray(4).apply {
            this[detectDirection(currentCoordinates, previousCoordinates)] = true
        }

    // Static
    fun detectTwoMargins(previousCoordinates: IntArray, currentCoordinates: IntArray, nextCoordinates: IntArray): BooleanArray =
        BooleanArray(4).apply {
            this[detectDirection(previousCoordinates, currentCoordinates)] = true
            this[detectDirection(nextCoordinates, currentCoordinates)] = true
        }
}
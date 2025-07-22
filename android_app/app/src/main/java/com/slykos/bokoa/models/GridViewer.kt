package com.slykos.bokoa.models

import android.content.res.ColorStateList
import android.graphics.Typeface
import androidx.gridlayout.widget.GridLayout
import com.slykos.bokoa.pagesHandler.GenericPlayPage

class GridViewer(private var context: GenericPlayPage, private val gridSize: IntArray, private val operations: Array<Array<String>>, mainTypeface: Typeface, mediumColor: ColorStateList, private val marginSize: Int, private val caseSize : Int){

    private val grid:Array<Array<CaseViewer?>> =
        Array(gridSize[1]) {
            arrayOfNulls(
                gridSize[0]
            )
        }

    init {
        for (i in 0 until gridSize[1]) {
            for (j in 0 until gridSize[0]) {
                this.grid[i][j] = CaseViewer(this.context,i,j,operations[i][j],gridSize,mainTypeface,mediumColor)
                context.getGameGrid().addView(this.grid[i][j]!!.caseRepresentation, getGridParams(i, j))
            }
        }
        this.shapeGrid()
    }

    private fun getGridParams(i: Int, j: Int): GridLayout.LayoutParams =
        GridLayout.LayoutParams().apply {
            setMargins(marginSize, marginSize, marginSize, marginSize)
            width = caseSize
            height = caseSize
            rowSpec = GridLayout.spec(i)
            columnSpec = GridLayout.spec(j)
        }

    fun emptyGrid() {
        for (i in 0 until gridSize[1]) {
            for (j in 0 until gridSize[0]) {
                context.getGameGrid().removeView(this.grid[i][j]!!.caseRepresentation)
            }
        }
    }

    fun shapeGrid() {
        for (i in 0 until gridSize[1]) {
            for (j in 0 until gridSize[0]) {
                if (operations[i][j] == "1") {
                    this.grid[i][j]!!.shapeNeutralCaseNeverMoved()
                } else {
                    this.grid[i][j]!!.shapeUnusedCase()
                }
            }
        }
    }

    fun getCase(i: Int, j: Int): CaseViewer =
        this.grid[i][j]!!

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
    fun detectSingleMargin(prev: IntArray, current: IntArray): BooleanArray =
        BooleanArray(4).apply {
            this[detectDirection(current, prev)] = true
        }

    // Static
    fun detectTwoMargins(prev: IntArray, current: IntArray, next: IntArray): BooleanArray =
        BooleanArray(4).apply {
            this[detectDirection(prev, current)] = true
            this[detectDirection(next, current)] = true
        }
}
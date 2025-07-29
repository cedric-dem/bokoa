package com.slykos.bokoa.models

import android.content.res.ColorStateList
import android.graphics.Typeface
import android.util.Log
import com.slykos.bokoa.models.viewers.CaseViewer
import com.slykos.bokoa.models.viewers.GridViewer
import com.slykos.bokoa.pagesHandler.playPages.GenericPlayPage
import kotlin.math.min
import kotlin.math.roundToInt

class GridHandler(
    private val context: GenericPlayPage,
    private val operationsGrid: Array<Array<String>>,
    private val gridSize: IntArray,
    private val mainTypeface: Typeface,
    private val mediumColor: ColorStateList,
    private val screenDimensions: IntArray
) {
    private lateinit var gridViewer: GridViewer

    private val caseSize: Int = min(
        ((screenDimensions[0] * 0.7) / gridSize[0]),
        ((screenDimensions[1] * 0.48) / gridSize[1])
    ).roundToInt()
    private val caseTextSize: Int = ((caseSize.toFloat() / 3.5) + -9.7).toInt()

    fun shapeGrid() {
        this.gridViewer.shapeGrid()
    }

    fun emptyGrid() {
        this.gridViewer.emptyGrid()
    }

    fun createGrid() {
        gridViewer = GridViewer(this.context, this.gridSize, operationsGrid, mainTypeface, mediumColor, caseSize, caseTextSize)
    }

    fun getCase(coordinates: IntArray): CaseViewer =
        gridViewer.getCase(coordinates)

    fun detectSingleMargin(previousCoordinates: IntArray, currentCoordinates: IntArray): BooleanArray =
        gridViewer.detectSingleMargin(previousCoordinates, currentCoordinates)

    fun detectTwoMargins(previousCoordinates: IntArray, currentCoordinates: IntArray, nextCoordinates: IntArray): BooleanArray =
        gridViewer.detectTwoMargins(previousCoordinates, currentCoordinates, nextCoordinates)

    fun getOperation(coordinates: IntArray): String =
        operationsGrid[coordinates[0]][coordinates[1]]

}
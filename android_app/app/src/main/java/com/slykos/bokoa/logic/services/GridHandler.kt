package com.slykos.bokoa.logic.services

import android.content.res.ColorStateList
import android.graphics.Typeface
import com.slykos.bokoa.frontend.view.CaseViewer
import com.slykos.bokoa.frontend.view.GridViewer
import com.slykos.bokoa.logic.game.GameUi
import com.slykos.bokoa.frontend.pages.playPages.GenericPlayPage
import com.slykos.bokoa.logic.models.Operation
import kotlin.math.min
import kotlin.math.roundToInt

class GridHandler(
    private val ui: GameUi,
    private val operationsGrid: Array<Array<Operation>>,
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
        gridViewer = GridViewer(this.ui as GenericPlayPage, this.gridSize, operationsGrid, mainTypeface, mediumColor, caseSize, caseTextSize)
    }

    fun getCase(coordinates: IntArray): CaseViewer =
        gridViewer.getCase(coordinates)

    private fun detectSingleMargin(previousCoordinates: IntArray, currentCoordinates: IntArray): BooleanArray =
        gridViewer.detectSingleMargin(previousCoordinates, currentCoordinates)

    private fun detectTwoMargins(previousCoordinates: IntArray, currentCoordinates: IntArray, nextCoordinates: IntArray): BooleanArray =
        gridViewer.detectTwoMargins(previousCoordinates, currentCoordinates, nextCoordinates)

    fun getOperation(coordinates: IntArray): Operation =
        operationsGrid[coordinates[0]][coordinates[1]]

    fun refreshBackground(coordinatesHistory: MutableList<IntArray>) { //todo move lot of computation in gridhandler

        // Inside
        for (i in 1 until coordinatesHistory.size - 1) { // start from first non neutral, until cursor
            getCase(coordinatesHistory[i]).shapeInHistoryCase(detectTwoMargins(coordinatesHistory[i - 1], coordinatesHistory[i], coordinatesHistory[i + 1]), ((255 * i) / coordinatesHistory.size))
        }

        if (coordinatesHistory.size > 1) { // cursor + neutral if more than one elem
            // Neutral
            getCase(coordinatesHistory[0]).shapeNeutralCase(detectSingleMargin(coordinatesHistory[0], coordinatesHistory[1]))

            // cursor
            getCase(coordinatesHistory.last()).shapeCursorCase(detectSingleMargin(coordinatesHistory.last(), coordinatesHistory[coordinatesHistory.size - 2]))

        } else { //if size 0, shape neutral only
            getCase(coordinatesHistory[0]).shapeNeutralCaseNeverMoved()
        }
    }

}
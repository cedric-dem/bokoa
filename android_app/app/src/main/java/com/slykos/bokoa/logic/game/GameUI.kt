package com.slykos.bokoa.logic.game

import android.content.Context
import android.view.View

interface GameUi {
    val context: Context
    fun refreshProgressBar(progression: Int)
    fun updateProgressBarTint(isFinished: Boolean)
    fun getMainView(): View
    fun getScreenDimensions(): IntArray
    fun finishedGame()
}

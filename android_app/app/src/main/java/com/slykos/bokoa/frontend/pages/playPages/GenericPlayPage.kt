package com.slykos.bokoa.frontend.pages.playPages

import android.content.res.ColorStateList
import android.util.DisplayMetrics
import android.view.View
import android.widget.ProgressBar
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.gridlayout.widget.GridLayout
import com.slykos.bokoa.R

abstract class GenericPlayPage : AppCompatActivity() {

    internal lateinit var mainLayout: View
    internal lateinit var gameGridLayout: GridLayout
    internal lateinit var scoreProgressBar: ProgressBar
    internal lateinit var displayMetrics: DisplayMetrics

    fun refreshProgressBar(progression: Int) {
        getProgressbar().progress = progression
    }

    fun updateProgressBarTint(isFinished: Boolean) {
        getProgressbar().progressTintList = ColorStateList.valueOf(
            if (isFinished) {
                ContextCompat.getColor(this, R.color.finished_color)
            } else {
                ContextCompat.getColor(this, R.color.light_color)
            }.toInt()
        )
    }

    fun getScreenDimensions(): IntArray =
        intArrayOf(displayMetrics.widthPixels, displayMetrics.heightPixels)

    abstract fun getProgressbar(): ProgressBar

    abstract fun getGameGrid(): GridLayout

    abstract fun getMainView(): View

    abstract fun finishedGame()
}

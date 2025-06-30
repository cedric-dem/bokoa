package com.slykos.bokoa.pagesHandler

import android.content.res.ColorStateList
import android.util.DisplayMetrics
import android.view.View
import android.widget.ProgressBar
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.gridlayout.widget.GridLayout
import com.slykos.bokoa.R

abstract class GenericPlayPage : AppCompatActivity() {

    internal lateinit var mainView: View
    internal lateinit var mainLayout: GridLayout
    internal lateinit var progressBarView: ProgressBar
    internal lateinit var displayMetrics: DisplayMetrics

    fun refreshProgressBar(progression: Int) {
        getProgressbar().progress = progression
        // getProgressbar().progressTintList = ColorStateList.valueOf(getGreenShade(progression))
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

    private fun getGreenShade(intensity: Int): Int {
        val dimmed = 255 - (intensity.coerceIn(0, 100) * 255 / 100)
        return (0xFF shl 24) or (dimmed shl 16) or (0xFF shl 8) or dimmed
    }

    fun getScreenDimensions(): IntArray =
        intArrayOf(displayMetrics.widthPixels, displayMetrics.heightPixels)

    abstract fun getProgressbar(): ProgressBar

    abstract fun getGameGrid(): GridLayout

    abstract fun getMainView(): View

    abstract fun finishedGame()
}

package com.slykos.bokoa.frontend.pages.playPages

import android.content.res.ColorStateList
import android.util.DisplayMetrics
import android.view.View
import android.widget.ProgressBar
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.gridlayout.widget.GridLayout
import com.slykos.bokoa.R

import com.slykos.bokoa.logic.game.GameUi

abstract class GenericPlayPage : AppCompatActivity(), GameUi {

    internal lateinit var mainLayout: View
    internal lateinit var gameGridLayout: GridLayout
    internal lateinit var scoreProgressBar: ProgressBar
    internal lateinit var displayMetrics: DisplayMetrics

    override val context = this

    override fun refreshProgressBar(progression: Int) {
        getProgressbar().progress = progression
    }

    override fun updateProgressBarTint(isFinished: Boolean) {
        getProgressbar().progressTintList = ColorStateList.valueOf(
            if (isFinished) {
                ContextCompat.getColor(this, R.color.finished_color)
            } else {
                ContextCompat.getColor(this, R.color.light_color)
            }.toInt()
        )
    }

    override fun getScreenDimensions(): IntArray =
        intArrayOf(displayMetrics.widthPixels, displayMetrics.heightPixels)

    abstract fun getProgressbar(): ProgressBar

    abstract fun getGameGrid(): GridLayout

    abstract override fun getMainView(): View

    abstract override fun finishedGame()


}
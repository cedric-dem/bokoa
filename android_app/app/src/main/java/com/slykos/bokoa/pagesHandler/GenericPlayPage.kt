package com.slykos.bokoa.pagesHandler

import android.content.Context
import android.content.res.ColorStateList
import android.util.DisplayMetrics
import android.view.View
import android.widget.ProgressBar
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.gridlayout.widget.GridLayout
import com.google.gson.Gson
import com.slykos.bokoa.R
import com.slykos.bokoa.models.Level
import java.io.InputStreamReader

abstract class GenericPlayPage : AppCompatActivity() {

    internal lateinit var mainView: View
    internal lateinit var mainLayout: GridLayout
    internal lateinit var progressBarView: ProgressBar
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

    protected fun loadLevelFromJson(context: Context, filename: String): Level? =
        try {
            val reader = InputStreamReader(context.assets.open(filename))

            Gson().fromJson(reader, Level::class.java).also {
                reader.close()
            }
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
}

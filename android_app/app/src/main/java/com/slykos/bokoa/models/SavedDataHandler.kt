package com.slykos.bokoa.models

import android.content.Context
import android.content.SharedPreferences

class SavedDataHandler(context: Context) {

    private val sharedPreferences: SharedPreferences = context.getSharedPreferences("sharedPrefs", Context.MODE_PRIVATE)
    private val editor = sharedPreferences.edit()

    fun getPassedLevels(): Int =
        sharedPreferences.getInt("passed_levels", 0)

    fun setPassedLevels(newPassedLevel: Int) {
        editor.putInt("passed_levels", newPassedLevel)
        editor.apply()
    }

    fun cheat() {
        setPassedLevels(300)
    }

    fun setEverPlayed() {
        editor.putBoolean("ever_played", true)
        editor.apply()
    }

    fun getEverPlayed(): Boolean =
        sharedPreferences.getBoolean("ever_played", false)
}

package com.slykos.bokoa.data.user

import android.content.Context
import android.content.SharedPreferences

class SavedDataHandler(context: Context) : UserRepository {

    private val sharedPreferences: SharedPreferences = context.getSharedPreferences("sharedPrefs", Context.MODE_PRIVATE)
    private val editor = sharedPreferences.edit()

    override fun getPassedLevels(): Int =
        sharedPreferences.getInt("passed_levels", 0)

    override fun setPassedLevels(newPassedLevel: Int) {
        editor.putInt("passed_levels", newPassedLevel)
        editor.apply()
    }

    fun cheat() {
        setPassedLevels(300)
    }

    override fun setEverPlayed() {
        editor.putBoolean("ever_played", true)
        editor.apply()
    }

    override fun getEverPlayed(): Boolean =
        sharedPreferences.getBoolean("ever_played", false)
}

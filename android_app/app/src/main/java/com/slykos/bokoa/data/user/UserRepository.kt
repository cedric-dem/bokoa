package com.slykos.bokoa.data.user

interface UserRepository {
    fun getPassedLevels(): Int
    fun setPassedLevels(newPassedLevel: Int)
    fun setEverPlayed()
    fun getEverPlayed(): Boolean
}
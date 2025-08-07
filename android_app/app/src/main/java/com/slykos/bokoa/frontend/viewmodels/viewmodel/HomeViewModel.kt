package com.slykos.bokoa.frontend.viewmodels.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.slykos.bokoa.config.Config
import com.slykos.bokoa.data.user.UserRepository

class HomeViewModel(private val userRepository: UserRepository) : ViewModel() {

    private val totalLevels = Config.NUMBER_OF_DIFFICULTIES * Config.LEVELS_PER_DIFFICULTIES

    private val _score = MutableLiveData<String>()
    val score: LiveData<String> = _score

    private val _launchTutorial = MutableLiveData<Boolean>()
    val launchTutorial: LiveData<Boolean> = _launchTutorial

    fun refreshScore() {
        val passed = userRepository.getPassedLevels()
        _score.value = "$passed/$totalLevels"
    }

    fun launchTutorialIfNeeded() {
        if (!userRepository.getEverPlayed()) {
            userRepository.setEverPlayed()
            _launchTutorial.value = true
        }
    }

    fun cheat() {
        userRepository.setPassedLevels(300)
    }
}
package com.slykos.bokoa.frontend.viewmodels.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.slykos.bokoa.config.Config
import com.slykos.bokoa.data.user.UserRepository

class DifficultySelectionViewModel(private val userRepository: UserRepository) : ViewModel() {

    data class DifficultyState(val difficulty: Int, val accessible: Boolean)

    private val _difficultyStates = MutableLiveData<List<DifficultyState>>()
    val difficultyStates: LiveData<List<DifficultyState>> = _difficultyStates

    fun loadDifficultyStates() {
        val passedLevels = userRepository.getPassedLevels()
        val states = (0 until Config.NUMBER_OF_DIFFICULTIES).map { difficulty ->
            DifficultyState(
                difficulty = difficulty,
                accessible = passedLevels >= (Config.LEVELS_PER_DIFFICULTIES * difficulty)
            )
        }
        _difficultyStates.value = states
    }
}
package com.slykos.bokoa.frontend.viewmodels.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.slykos.bokoa.config.Config
import com.slykos.bokoa.data.user.UserRepository

class LevelSelectionViewModel(private val userRepository: UserRepository) : ViewModel() {

    data class LevelState(val level: Int, val accessible: Boolean)

    private val _levelStates = MutableLiveData<List<LevelState>>()
    val levelStates: LiveData<List<LevelState>> = _levelStates

    fun loadLevelStates(difficulty: Int) {
        val passedLevels = userRepository.getPassedLevels()
        val states = (0 until Config.LEVELS_PER_DIFFICULTIES).map { index ->
            val globalLevel = Config.LEVELS_PER_DIFFICULTIES * difficulty + index
            LevelState(
                level = index,
                accessible = passedLevels >= globalLevel
            )
        }
        _levelStates.value = states
    }
}

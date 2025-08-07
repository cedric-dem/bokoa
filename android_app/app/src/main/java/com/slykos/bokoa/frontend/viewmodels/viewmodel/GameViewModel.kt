package com.slykos.bokoa.frontend.viewmodels.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.slykos.bokoa.R
import com.slykos.bokoa.config.Config
import com.slykos.bokoa.data.levels.loadLevelFromJson
import com.slykos.bokoa.data.user.UserRepository
import android.content.Context
import com.slykos.bokoa.logic.game.Game
import com.slykos.bokoa.logic.game.GameUi
import com.slykos.bokoa.logic.game.RealGame
import com.slykos.bokoa.logic.models.Level

class GameViewModel(private val userRepository: UserRepository) : ViewModel() {

    private lateinit var appContext: Context
    private lateinit var currentGame: Game
    private lateinit var currentLevel: Level

    private var levelId: Int = 0
    private var difficulty: Int = 0
    private var passedLevels: Int = 0
    private val finishedGameAt = (Config.NUMBER_OF_DIFFICULTIES * Config.LEVELS_PER_DIFFICULTIES) - 1

    private val _title = MutableLiveData<String>()
    val title: LiveData<String> = _title

    private val _topText = MutableLiveData<String>()
    val topText: LiveData<String> = _topText

    private val _bottomText = MutableLiveData<String>()
    val bottomText: LiveData<String> = _bottomText

    private val _nextLevelAvailable = MutableLiveData<Boolean>()
    val nextLevelAvailable: LiveData<Boolean> = _nextLevelAvailable

    fun startGame(ui: GameUi, level: Int, diff: Int) {
        appContext = ui.context
        levelId = level
        difficulty = diff

        currentGame = RealGame(ui) { scoreString ->
            _topText.value = appContext.getString(R.string.score)
            _bottomText.value = scoreString
        }

        runGame()
    }

    private fun initLevel() {
        val paddedLevelId = levelId.toString().padStart(6, '0')
        val fileName = "grid_size_$difficulty/level_$paddedLevelId.json"
        currentLevel = loadLevelFromJson(appContext, fileName)!!

        passedLevels = userRepository.getPassedLevels()
        val available = passedLevels > difficulty * Config.LEVELS_PER_DIFFICULTIES + levelId
        _nextLevelAvailable.value = available

        currentGame.initLevel(Config.GRID_SIZES[difficulty], currentLevel)
    }

    private fun runGame() {
        initLevel()
        _title.value =
            appContext.getString(R.string.level) +
                    (difficulty * Config.LEVELS_PER_DIFFICULTIES + levelId + 1).toString() +
                    "\n" + appContext.getString(R.string.difficulty) + ": " +
                    Config.DIFFICULTIES_NAMES[difficulty]

        currentGame.runGame()

        if (Config.SHOW_SOLUTION_AT_START) {
            solve()
        }
    }

    fun nextLevel() {
        if (_nextLevelAvailable.value != true) {
            return
        }

        currentGame.emptyGrid()

        levelId += 1
        if (levelId == Config.LEVELS_PER_DIFFICULTIES) {
            levelId = 0
            difficulty += 1
        }

        runGame()
    }

    fun resetGame() {
        currentGame.initGame()
        currentGame.shapeGrid()
        currentGame.refreshScore()
    }

    fun solve() {
        resetGame()
        for (move in currentLevel.bestMoves) {
            currentGame.applyMove(move)
        }
    }

    fun moveUp() = currentGame.moveUp()
    fun moveDown() = currentGame.moveDown()
    fun moveLeft() = currentGame.moveLeft()
    fun moveRight() = currentGame.moveRight()
    fun checkGoalReached(): Boolean = currentGame.checkGoalReached()

    fun finishedGame() {
        if (passedLevels == difficulty * Config.LEVELS_PER_DIFFICULTIES + levelId) {
            wonFirstTimeLevel()
        } else {
            wonLevelAgain()
        }
    }

    private fun wonLevelAgain() {
        _topText.value =
            appContext.getString(R.string.finished_level_again) + currentGame.getBestScoreString()
        _bottomText.value = ""
    }

    private fun wonFirstTimeLevel() {
        _topText.value =
            appContext.getString(R.string.finished_level) + currentGame.getBestScoreString()

        if ((passedLevels + 1) % Config.LEVELS_PER_DIFFICULTIES == 0) {
            if (passedLevels == finishedGameAt) {
                _bottomText.value = appContext.getString(R.string.finished_all_levels)
            } else {
                _bottomText.value =
                    appContext.getString(R.string.difficulty) +
                            Config.DIFFICULTIES_NAMES[(passedLevels / Config.LEVELS_PER_DIFFICULTIES) + 1] +
                            " " + appContext.getString(R.string.difficulty_unlocked)
                _nextLevelAvailable.value = true
            }
        } else {
            _bottomText.value =
                appContext.getString(R.string.level) + (passedLevels + 2).toString() +
                        " " + appContext.getString(R.string.level_unlocked)
            _nextLevelAvailable.value = true
        }

        passedLevels += 1
        userRepository.setPassedLevels(passedLevels)
    }
}

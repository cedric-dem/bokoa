package com.slykos.bokoa.pagesHandler

import android.app.AlertDialog
import android.os.Bundle
import android.view.KeyEvent
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.gridlayout.widget.GridLayout
import com.google.android.gms.ads.AdRequest
import com.google.android.gms.ads.LoadAdError
import com.google.android.gms.ads.rewarded.RewardedAd
import com.google.android.gms.ads.rewarded.RewardedAdLoadCallback
import com.google.android.material.snackbar.Snackbar
import com.slykos.bokoa.R
import com.slykos.bokoa.models.AdHandler
import com.slykos.bokoa.models.game.Game
import com.slykos.bokoa.models.Level
import com.slykos.bokoa.models.game.RealGame
import com.slykos.bokoa.models.SavedDataHandler

open class GamePageHandler : GenericPlayPage() {
    private lateinit var scoreIndicatorTop: TextView
    private lateinit var scoreIndicatorBottom: TextView
    private lateinit var title: TextView
    private lateinit var adButton: Button
    private lateinit var buttonNextLevel: Button
    private lateinit var currentLevel: Level
    private lateinit var gridSize: IntArray
    private var gridSizes: IntArray = intArrayOf()
    private var levelId: Int = 0
    private var difficulty: Int = 0
    private var passedLevels: Int = 0
    private var levelsPerDifficulty: Int = 0
    private var finishedGameAt: Int = 0
    private var extras: Bundle? = null

    private lateinit var savedDataHandler: SavedDataHandler

    private var levelsSectionsNames: Array<String> = arrayOf()
    private lateinit var currentGame: Game

    private lateinit var le_ad_handler: AdHandler;

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_in_game)

        // ////////////////////////////////////////////////////////////////////////////////// Identifying and doing things wid tem layout

        savedDataHandler = SavedDataHandler(this)

        initializePage()

        currentGame = RealGame(this)

        // //////////////////////////////////////////////////////// Initiate Ad and confirmation popup
        le_ad_handler = AdHandler(this, adButton)

        // //////////////////////////////////////////////////// Obtain level and difficulty
        getExtras()

        // //////////////////////////////////////////////////// Top bar

        runGame()

        // showSolution(); //FOR DEBUG 4/5
    }

    fun showSolution() {
        // Restart
        resetGame()

        // Go trough optimal moves
        for (i in currentLevel.bestMoves.indices) {
            currentGame.applyMove(currentLevel.bestMoves[i])
        }
    }

    private fun resetGame() {
        currentGame.initGame()
        currentGame.shapeGrid()
        currentGame.refreshScore()
    }

    private fun runGame() {
        initLevel()

        title.text = getString(R.string.level) + (difficulty * levelsPerDifficulty + levelId + 1).toString() + "\n" + getString(
            R.string.difficulty
        ) + ": " + levelsSectionsNames[difficulty]

        // current_game.initLevel(grid_size, current_level);
        currentGame.runGame()
    }

    private fun makeNextLevelButtonEffective() {
        // change icon
        buttonNextLevel.foreground = ContextCompat.getDrawable(this, R.drawable.icon_next_unlocked)

        // onclick call next level
        buttonNextLevel.setOnClickListener { nextLevel() }
    }

    private fun makeNextLevelButtonIneffective() {
        // change icon
        buttonNextLevel.foreground = ContextCompat.getDrawable(this, R.drawable.icon_next_locked)

        // onclick do not call nextLevel. maybe set button ineffective ?
        buttonNextLevel.setOnClickListener {
            Snackbar.make(getGameGrid(), getString(R.string.info_locked), 3000).show()
        }
    }

    private fun nextLevel() {
        // empty grid
        currentGame.emptyGrid()

        // load level n+1
        levelId += 1

        if (levelId == levelsPerDifficulty) {
            levelId = 0
            difficulty += 1
        }
        runGame()

        // maybe finish() add param difficulty +1 onCreate
    }

    private fun initLevel() {
        val paddedLevelId = levelId.toString().padStart(6, '0')
        val fileName = "grid_size_$difficulty/level_$paddedLevelId.json"
        currentLevel = this.loadLevelFromJson(this, fileName)!!

        gridSize = intArrayOf(gridSizes[difficulty], gridSizes[difficulty])

        passedLevels = savedDataHandler.getPassedLevels()

        if (passedLevels > difficulty * levelsPerDifficulty + levelId) {
            makeNextLevelButtonEffective()
        } else {
            makeNextLevelButtonIneffective()
        }

        currentGame.initLevel(gridSize, currentLevel)
    }

    private fun hasPassedThisLevel(): Boolean =
        (passedLevels == difficulty * levelsPerDifficulty + levelId)

    override fun finishedGame() {
        if (hasPassedThisLevel()) {
            wonFirstTimeLevel()
        } else {
            wonLevelAgain()
        }
    }

    private fun wonLevelAgain() {
        scoreIndicatorTop.text = getString(R.string.finished_level_again) + currentGame.bestScoreStr
        scoreIndicatorBottom.text = ""
    }

    private fun wonFirstTimeLevel() {
        // ////////////////////////////////////////////////////////////////////////////////////////// TOP text
        scoreIndicatorTop.text = getString(R.string.finished_level) + currentGame.bestScoreStr

        // ////////////////////////////////////////////////////////////////////////////////////////// detect case then  BOT text +  BTN effective
        if ((passedLevels + 1) % levelsPerDifficulty == 0) {
            if (passedLevels == finishedGameAt) { // finished game
                scoreIndicatorBottom.text = getString(R.string.finished_all_levels)
            } else { // difficulty unlocked
                scoreIndicatorBottom.text = getString(R.string.difficulty) + levelsSectionsNames[(passedLevels / levelsPerDifficulty) + 1] + " " + getString(
                    R.string.difficulty_unlocked
                )
                makeNextLevelButtonEffective()
            }
        } else {
            scoreIndicatorBottom.text = getString(R.string.level) + (passedLevels + 2).toString() + " " + getString(R.string.level_unlocked)
            makeNextLevelButtonEffective()
        }

        // ////////////////////////////////////////////////////////////////////////////////////////// SAVE PROGRESS
        passedLevels += 1
        savedDataHandler.setPassedLevels(passedLevels)
    }

    private fun initializePage() {
        // gridSizes = resources.getIntArray(R.array.grid_size)
        gridSizes = resources.getIntArray(R.array.grid_sizes)

        levelsSectionsNames = resources.getStringArray(R.array.difficulty_names)
        levelsPerDifficulty = resources.getInteger(R.integer.levels_per_difficulty)
        finishedGameAt = (resources.getInteger(R.integer.number_of_difficulty) * levelsPerDifficulty) - 1

        extras = intent.extras
        displayMetrics = resources.displayMetrics

        mainView = findViewById(R.id.ml)
        mainLayout = findViewById(R.id.game_board)

        title = findViewById(R.id.page_title)

        // //////////////////////////////////////////////////// Score
        scoreIndicatorTop = findViewById(R.id.score_indicator_top)
        scoreIndicatorBottom = findViewById(R.id.score_indicator_bottom)

        progressBarView = findViewById(R.id.progress_bar)

        adButton = findViewById(R.id.button_ad)

        // makeAdButtonEffective(); //FOR DEBUG 1/5
        buttonNextLevel = findViewById(R.id.next_level)

        findViewById<Button>(R.id.button_reset).setOnClickListener { resetGame() }
        // findViewById<Button>(R.id.button_reset).setOnClickListener {showSolution() } //for debug 5/5

        findViewById<Button>(R.id.button_back).setOnClickListener { finish() }
    }

    private fun getExtras() {
        levelId = extras!!.getInt("level")
        difficulty = extras!!.getInt("difficulty")
    }

    internal fun setScoreText(newText: String) {
        scoreIndicatorTop.text = resources.getString(R.string.score)
        scoreIndicatorBottom.text = newText
    }

    override fun getProgressbar(): ProgressBar =
        progressBarView

    override fun getGameGrid(): GridLayout =
        mainLayout

    override fun getMainView(): View =
        mainView

    override fun onKeyDown(keyCode: Int, event: KeyEvent?): Boolean {
        when (keyCode) {
            KeyEvent.KEYCODE_DPAD_UP -> {
                this.currentGame.moveUp()
                return true
            }

            KeyEvent.KEYCODE_DPAD_DOWN -> {
                this.currentGame.moveDown()
                return true
            }

            KeyEvent.KEYCODE_DPAD_LEFT -> {
                this.currentGame.moveLeft()
                return true
            }

            KeyEvent.KEYCODE_DPAD_RIGHT -> {
                this.currentGame.moveRight()
                return true
            }
        }
        return super.onKeyDown(keyCode, event)
    }
}

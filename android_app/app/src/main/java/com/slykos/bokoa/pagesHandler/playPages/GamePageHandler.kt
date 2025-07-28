package com.slykos.bokoa.pagesHandler.playPages

import android.os.Bundle
import android.view.KeyEvent
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.gridlayout.widget.GridLayout
import com.google.android.material.snackbar.Snackbar
import com.slykos.bokoa.Config
import com.slykos.bokoa.R
import com.slykos.bokoa.models.AdHandler
import com.slykos.bokoa.models.game.Game
import com.slykos.bokoa.models.Level
import com.slykos.bokoa.models.game.RealGame
import com.slykos.bokoa.models.SavedDataHandler

open class GamePageHandler : GenericPlayPage() {
    private lateinit var topScoreIndicatorTextView: TextView
    private lateinit var bottomScoreIndicatorTextView: TextView
    private lateinit var titleTextView: TextView
    private lateinit var adButton: Button
    private lateinit var nextLevelButton: Button

    private var levelId: Int = 0
    private var difficulty: Int = 0
    private var passedLevels: Int = 0
    private var finishedGameAt: Int = 0

    private var extras: Bundle? = null

    private lateinit var savedDataHandler: SavedDataHandler

    private lateinit var currentGame: Game
    private lateinit var currentLevel: Level

    private lateinit var adHandler: AdHandler;

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_in_game)

        savedDataHandler = SavedDataHandler(this)

        initializePage()

        currentGame = RealGame(this)

        adHandler = AdHandler(this, adButton)

        getExtras()

        runGame()

        if (Config.SHOW_SOLUTION_AT_START) {
            showSolution()
        }
        if (Config.SKIP_AD) {
            adHandler.makeAdButtonEffective();
        }
    }

    fun showSolution() {
        // Restart
        resetGame()

        // Go trough solution
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

        titleTextView.text = getString(R.string.level) + (difficulty * Config.LEVELS_PER_DIFFICULTIES + levelId + 1).toString() + "\n" + getString(
            R.string.difficulty
        ) + ": " + Config.DIFFICULTIES_NAMES[difficulty]

        // current_game.initLevel(grid_size, current_level);
        currentGame.runGame()
    }

    private fun makeNextLevelButtonEffective() {
        // change icon
        nextLevelButton.foreground = ContextCompat.getDrawable(this, R.drawable.icon_next_unlocked)

        // onclick call next level
        nextLevelButton.setOnClickListener { nextLevel() }
    }

    private fun makeNextLevelButtonIneffective() {
        // change icon
        nextLevelButton.foreground = ContextCompat.getDrawable(this, R.drawable.icon_next_locked)

        // onclick do not call nextLevel. maybe set button ineffective ?
        nextLevelButton.setOnClickListener {
            Snackbar.make(getGameGrid(), getString(R.string.info_locked), 3000).show()
        }
    }

    private fun nextLevel() {
        // empty grid
        currentGame.emptyGrid()

        // load level n+1
        levelId += 1

        if (levelId == Config.LEVELS_PER_DIFFICULTIES) {
            levelId = 0
            difficulty += 1
        }
        runGame()

        // TODO maybe finish() add param difficulty +1 onCreate
    }

    private fun initLevel() {
        val paddedLevelId = levelId.toString().padStart(6, '0')
        val fileName = "grid_size_$difficulty/level_$paddedLevelId.json"
        currentLevel = this.loadLevelFromJson(this, fileName)!!

        passedLevels = savedDataHandler.getPassedLevels()

        if (passedLevels > difficulty * Config.LEVELS_PER_DIFFICULTIES + levelId) {
            makeNextLevelButtonEffective()
        } else {
            makeNextLevelButtonIneffective()
        }

        currentGame.initLevel(Config.GRID_SIZES[difficulty], currentLevel)
    }

    private fun hasPassedThisLevel(): Boolean =
        (passedLevels == difficulty * Config.LEVELS_PER_DIFFICULTIES + levelId)

    override fun finishedGame() {
        if (hasPassedThisLevel()) {
            wonFirstTimeLevel()
        } else {
            wonLevelAgain()
        }
    }

    private fun wonLevelAgain() {
        topScoreIndicatorTextView.text = getString(R.string.finished_level_again) + currentGame.bestScoreString
        bottomScoreIndicatorTextView.text = ""
    }

    private fun wonFirstTimeLevel() {
        // Top text
        topScoreIndicatorTextView.text = getString(R.string.finished_level) + currentGame.bestScoreString

        // detect case then bottom text + next level button effective
        if ((passedLevels + 1) % Config.LEVELS_PER_DIFFICULTIES == 0) {
            if (passedLevels == finishedGameAt) { // finished game
                bottomScoreIndicatorTextView.text = getString(R.string.finished_all_levels)
            } else { // difficulty unlocked
                bottomScoreIndicatorTextView.text = getString(R.string.difficulty) + Config.DIFFICULTIES_NAMES[(passedLevels / Config.LEVELS_PER_DIFFICULTIES) + 1] + " " + getString(
                    R.string.difficulty_unlocked
                )
                makeNextLevelButtonEffective()
            }
        } else {
            bottomScoreIndicatorTextView.text = getString(R.string.level) + (passedLevels + 2).toString() + " " + getString(R.string.level_unlocked)
            makeNextLevelButtonEffective()
        }

        // Save progress
        passedLevels += 1
        savedDataHandler.setPassedLevels(passedLevels)
    }

    private fun initializePage() {
        finishedGameAt = (Config.NUMBER_OF_DIFFICULTIES * Config.LEVELS_PER_DIFFICULTIES) - 1

        extras = intent.extras
        displayMetrics = resources.displayMetrics

        mainLayout = findViewById(R.id.main_layout)
        gameGridLayout = findViewById(R.id.game_grid)

        titleTextView = findViewById(R.id.page_title)

        // Score
        topScoreIndicatorTextView = findViewById(R.id.score_indicator_top)
        bottomScoreIndicatorTextView = findViewById(R.id.score_indicator_bottom)

        scoreProgressBar = findViewById(R.id.progress_bar)

        adButton = findViewById(R.id.button_ad)

        nextLevelButton = findViewById(R.id.next_level)

        findViewById<Button>(R.id.button_reset).setOnClickListener { resetGame() }

        findViewById<Button>(R.id.button_back).setOnClickListener { finish() }
    }

    private fun getExtras() {
        levelId = extras!!.getInt("level")
        difficulty = extras!!.getInt("difficulty")
    }

    internal fun setScoreText(newText: String) {
        topScoreIndicatorTextView.text = resources.getString(R.string.score)
        bottomScoreIndicatorTextView.text = newText
    }

    override fun getProgressbar(): ProgressBar =
        scoreProgressBar

    override fun getGameGrid(): GridLayout =
        gameGridLayout

    override fun getMainView(): View =
        mainLayout

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

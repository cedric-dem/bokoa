package com.slykos.bokoa.frontend.pages.playPages

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.gridlayout.widget.GridLayout
import com.slykos.bokoa.R
import com.slykos.bokoa.data.levels.loadLevelFromJson
import com.slykos.bokoa.logic.game.Game
import com.slykos.bokoa.logic.models.Level
import com.slykos.bokoa.logic.game.TutorialGame

class TutorialPageHandler : GenericPlayPage() {
    private lateinit var tutorialGame: Game

    private lateinit var tipGiverTextView: TextView
    private lateinit var currentEquationTextView: TextView
    private lateinit var currentScoreTextView: TextView
    private lateinit var maxScoreTextView: TextView
    private lateinit var nextButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_tutorial)

        initializePage()

        // TODO remove code duplication on both

        tutorialGame = TutorialGame(this)

        tutorialGame.initLevel(intArrayOf(3, 3), getTutorialLevel())

        this.setMaxScore()

        tutorialGame.runGame()
    }

    override fun finishedGame() {
        // message highest score reached, no way to do better
        tipGiverTextView.text = getString(R.string.finished_tutorial)

        // button quit becomes continue
        nextButton.setTextColor(ContextCompat.getColor(this, R.color.light_color))
        nextButton.text = getString(R.string.continue_tutorial)
    }

    private fun initializePage() {
        displayMetrics = resources.displayMetrics

        findViewById<Button>(R.id.button_pass_tutorial).setOnClickListener { finish() }

        tipGiverTextView = findViewById(R.id.tip_text)

        currentEquationTextView = findViewById(R.id.equation_viewer)

        mainLayout = findViewById(R.id.main_layout)
        gameGridLayout = findViewById(R.id.game_grid)

        scoreProgressBar = findViewById(R.id.progress_bar)

        currentScoreTextView = findViewById(R.id.current_score_viewer)
        maxScoreTextView = findViewById(R.id.max_score_adv)

        nextButton = findViewById(R.id.button_pass_tutorial)
    }

    private fun getTutorialLevel(): Level =
        loadLevelFromJson(this, "tutorial/level_000000.json")!!

    fun setTip(newTip: String) {
        tipGiverTextView.text = newTip
    }

    fun setEquation(newTip: String) {
        currentEquationTextView.text = newTip
    }

    fun setCurrentScore(newScore: String) {
        currentScoreTextView.text = newScore
    }

    private fun setMaxScore() {
        maxScoreTextView.text = tutorialGame.bestScoreString
    }

    override fun getProgressbar(): ProgressBar =
        scoreProgressBar

    override fun getGameGrid(): GridLayout =
        gameGridLayout

    override fun getMainView(): View =
        mainLayout
}

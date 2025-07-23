package com.slykos.bokoa.pagesHandler

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.gridlayout.widget.GridLayout
import com.slykos.bokoa.R
import com.slykos.bokoa.models.game.Game
import com.slykos.bokoa.models.Level
import com.slykos.bokoa.models.game.TutorialGame

class TutorialPageHandler : GenericPlayPage() {
    private lateinit var tutorialGame: Game

    private lateinit var tipGiver: TextView
    private lateinit var equationView: TextView
    private lateinit var currentScoreViewer: TextView
    private lateinit var maxScoreViewer: TextView
    lateinit var next: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_tutorial)

        initializePage()

        // // TODO remove code duplication on both

        tutorialGame = TutorialGame(this)

        tutorialGame.initLevel(intArrayOf(3, 3), getTutorialLevel())
        tutorialGame.runGame()
    }

    override fun finishedGame() {
        // message highest score reached, no way to do better
        tipGiver.text = getString(R.string.finished_tutorial)

        // button quit becomes continue
        next.setTextColor(ContextCompat.getColor(this, R.color.light_color))
        next.text = getString(R.string.continue_tutorial)
    }

    private fun initializePage() {
        displayMetrics = resources.displayMetrics

        findViewById<Button>(R.id.button_pass_tutorial).setOnClickListener { finish() }

        tipGiver = findViewById(R.id.tip_giver)

        equationView = findViewById(R.id.equation_viewer)

        mainView = findViewById(R.id.ml)
        mainLayout = findViewById(R.id.game_board)

        progressBarView = findViewById(R.id.progress_bar)

        currentScoreViewer = findViewById(R.id.current_score_viewer)
        maxScoreViewer = findViewById(R.id.max_score_adv)

        next = findViewById(R.id.button_pass_tutorial)
    }

    private fun getTutorialLevel(): Level =
        this.loadLevelFromJson(this, "tutorial/level_000000.json")!!

    fun setTip(newTip: String) {
        tipGiver.text = newTip
    }

    fun setEquation(newTip: String) {
        equationView.text = newTip
    }

    fun setCurrentScore(newScore: String) {
        currentScoreViewer.text = newScore
    }

    fun setMaxScore(maxScore: String) {
        maxScoreViewer.text = maxScore
    }

    override fun getProgressbar(): ProgressBar =
        progressBarView

    override fun getGameGrid(): GridLayout =
        mainLayout

    override fun getMainView(): View =
        mainView
}

package com.slykos.bokoa.frontend.pages.playPages

import android.os.Bundle
import android.view.KeyEvent
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.gridlayout.widget.GridLayout
import androidx.lifecycle.ViewModelProvider
import com.google.android.material.snackbar.Snackbar
import com.slykos.bokoa.R
import com.slykos.bokoa.config.Config
import com.slykos.bokoa.data.user.SavedDataHandler
import com.slykos.bokoa.data.user.UserRepository
import com.slykos.bokoa.frontend.viewmodels.viewmodel.GameViewModel
import com.slykos.bokoa.frontend.viewmodels.viewmodelfactory.GameViewModelFactory
import com.slykos.bokoa.logic.services.AdHandler

open class GamePageHandler : GenericPlayPage() {
    private lateinit var topScoreIndicatorTextView: TextView
    private lateinit var bottomScoreIndicatorTextView: TextView
    private lateinit var titleTextView: TextView
    private lateinit var adButton: Button
    private lateinit var nextLevelButton: Button

    private lateinit var viewModel: GameViewModel
    private lateinit var adHandler: AdHandler

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_in_game)

        initializePage()

        val userRepository: UserRepository = SavedDataHandler(this)
        viewModel = ViewModelProvider(
            this,
            GameViewModelFactory(userRepository)
        )[GameViewModel::class.java]

        adHandler = AdHandler(this, adButton)

        val extras = intent.extras
        val level = extras!!.getInt("level")
        val difficulty = extras.getInt("difficulty")
        viewModel.startGame(this, level, difficulty)

        observeViewModel()

        if (Config.SKIP_AD) {
            adHandler.makeAdButtonEffective()
        }
    }

    fun solve() {
        viewModel.solve()
    }

    private fun makeNextLevelButtonEffective() {
        nextLevelButton.foreground = ContextCompat.getDrawable(this, R.drawable.icon_next_unlocked)
    }

    private fun makeNextLevelButtonIneffective() {
        nextLevelButton.foreground = ContextCompat.getDrawable(this, R.drawable.icon_next_locked)
    }

    private fun observeViewModel() {
        viewModel.title.observe(this) { title ->
            titleTextView.text = title
        }
        viewModel.topText.observe(this) { text ->
            topScoreIndicatorTextView.text = text
        }
        viewModel.bottomText.observe(this) { text ->
            bottomScoreIndicatorTextView.text = text
        }
        viewModel.nextLevelAvailable.observe(this) { available ->
            if (available) {
                makeNextLevelButtonEffective()
            } else {
                makeNextLevelButtonIneffective()
            }
        }
    }

    private fun initializePage() {
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

        findViewById<Button>(R.id.button_reset).setOnClickListener { viewModel.resetGame() }

        findViewById<Button>(R.id.button_back).setOnClickListener { finish() }

        nextLevelButton.setOnClickListener {
            if (viewModel.nextLevelAvailable.value == true) {
                viewModel.nextLevel()
            } else {
                Snackbar.make(getGameGrid(), getString(R.string.info_locked), 3000).show()
            }
        }
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
                viewModel.moveUp()
                return true
            }

            KeyEvent.KEYCODE_DPAD_DOWN -> {
                viewModel.moveDown()
                return true
            }

            KeyEvent.KEYCODE_DPAD_LEFT -> {
                viewModel.moveLeft()
                return true
            }

            KeyEvent.KEYCODE_DPAD_RIGHT -> {
                viewModel.moveRight()
                return true
            }
        }
        return super.onKeyDown(keyCode, event)
    }

    fun checkGoalReached(): Boolean =
        viewModel.checkGoalReached()

    override fun finishedGame() {
        viewModel.finishedGame()
    }

}
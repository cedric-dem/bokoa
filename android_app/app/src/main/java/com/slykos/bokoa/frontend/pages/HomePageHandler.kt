package com.slykos.bokoa.frontend.pages

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import com.slykos.bokoa.config.Config
import com.slykos.bokoa.R
import com.slykos.bokoa.data.user.SavedDataHandler
import com.slykos.bokoa.data.user.UserRepository
import com.slykos.bokoa.frontend.pages.playPages.TutorialPageHandler
import com.slykos.bokoa.frontend.viewmodels.viewmodel.HomeViewModel
import com.slykos.bokoa.frontend.viewmodels.viewmodelfactory.HomeViewModelFactory
import kotlin.system.exitProcess

class HomePageHandler : AppCompatActivity() {
    private lateinit var viewModel: HomeViewModel
    private lateinit var passedLevelsTextView: TextView

    public override fun onResume() {
        super.onResume()
        viewModel.refreshScore()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)

        val userRepository: UserRepository = SavedDataHandler(this)
        viewModel = ViewModelProvider(
            this,
            HomeViewModelFactory(userRepository)
        )[HomeViewModel::class.java]

        passedLevelsTextView = findViewById(R.id.display_score)

        observeViewModel()

        viewModel.launchTutorialIfNeeded()

        initializePage()

        if (Config.PASS_ALL_LEVELS) {
            viewModel.cheat()
        }
    }

    private fun initializePlayButton() {
        findViewById<Button>(R.id.button_play).setOnClickListener {
            startActivity(
                Intent(
                    applicationContext,
                    DifficultySelectionPageHandler::class.java
                )
            )
        }
    }

    private fun initializeHelpButton() {
        findViewById<Button>(R.id.button_tutorial).setOnClickListener {
            startActivity(
                Intent(
                    applicationContext,
                    HowToPlayPageHandler::class.java
                )
            )
        }
    }

    private fun initializeQuitButton() {
        findViewById<Button>(R.id.button_quit).setOnClickListener {
            finish()
            exitProcess(0)
        }
    }

    private fun observeViewModel() {
        viewModel.score.observe(this) { score ->
            passedLevelsTextView.text = getString(R.string.passed_levels) + score
        }
        viewModel.launchTutorial.observe(this) { launch ->
            if (launch) {
                startActivity(
                    Intent(
                        applicationContext,
                        TutorialPageHandler::class.java
                    )
                )
            }
        }
    }

    private fun initializePage() {
        initializePlayButton()
        initializeHelpButton()
        initializeQuitButton()
        viewModel.refreshScore()
    }
}
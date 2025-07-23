package com.slykos.bokoa.pagesHandler

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.slykos.bokoa.R
import com.slykos.bokoa.models.SavedDataHandler
import kotlin.system.exitProcess

class HomePageHandler : AppCompatActivity() {
    private var totalLevels: Int = 0
    private lateinit var scoreDisplay: TextView
    private lateinit var savedDataHandler: SavedDataHandler

    public override fun onResume() {
        super.onResume()
        refreshScore()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)

        savedDataHandler = SavedDataHandler(this)

        launchTutorialIfNeeded()

        initializePage()

        // savedDataHandler.cheat() // FOR DEBUG 3/5
    }

    private fun refreshScore() {
        scoreDisplay = findViewById(R.id.display_score)
        scoreDisplay.text =getString(R.string.passed_levels) + savedDataHandler.getPassedLevels().toString() + "/" + totalLevels.toString()
    }

    private fun launchTutorialIfNeeded() {
        if (!savedDataHandler.getEverPlayed()) {
            savedDataHandler.setEverPlayed()

            startActivity(
                Intent(
                    applicationContext,
                    TutorialPageHandler::class.java
                )
            )
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

    private fun initializePage() {
        totalLevels = (resources.getInteger(R.integer.number_of_difficulty) * resources.getInteger(R.integer.levels_per_difficulty))

        refreshScore()

        initializePlayButton()
        initializeHelpButton()
        initializeQuitButton()
    }
}

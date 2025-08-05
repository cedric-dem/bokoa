package com.slykos.bokoa.frontend.pages

import com.slykos.bokoa.config.Config
import android.content.Intent
import android.os.Bundle
import android.util.TypedValue
import android.widget.Button
import android.widget.LinearLayout
import android.widget.Space
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.slykos.bokoa.R
import com.slykos.bokoa.data.user.SavedDataHandler

class DifficultySelectionPageHandler : AppCompatActivity() {

    private lateinit var savedDataHandler: SavedDataHandler

    public override fun onResume() {
        super.onResume()
        // TODO set difficulty
        configureDifficultyButtons()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_difficulty_selection)

        savedDataHandler = SavedDataHandler(this)

        initializePage()

        // configureDifficultyButtons called by onResume;
    }

    private fun getWeightLayoutParameter(): LinearLayout.LayoutParams =
        LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.MATCH_PARENT,
            1.0f
        )

    private fun createDifficultyButtons(difficultyButtonsLayout: LinearLayout, difficulty: Int) {
        val button = Button(this).apply {
            id = 2000 + difficulty
            text = Config.DIFFICULTIES_NAMES[difficulty]
            setTextColor(ContextCompat.getColor(this@DifficultySelectionPageHandler, R.color.light_color))
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 23f)
            typeface = resources.getFont(R.font.main_font)
        }

        difficultyButtonsLayout.addView(button, getWeightLayoutParameter())

        val space = Space(this).apply {
            minimumHeight = 30
        }

        difficultyButtonsLayout.addView(space)
    }

    private fun goToLevelSelection(difficulty: Int) {
        val switchActivityIntent = Intent(applicationContext, LevelSelectionPageHandler::class.java)

        switchActivityIntent.putExtra("difficulty", difficulty)

        startActivity(switchActivityIntent)
    }

    private fun configureDifficultyButtons() {
        val passedLevels = savedDataHandler.getPassedLevels()

        var currentButton: Button

        for (currentDifficulty in 0 until Config.NUMBER_OF_DIFFICULTIES) { // difficulty

            currentButton = findViewById(2000 + currentDifficulty)

            if (passedLevels < (Config.LEVELS_PER_DIFFICULTIES * currentDifficulty)) { // Not accessible
                setDifficultyButtonNotAccessible(currentButton)

            } else { // accessible
                setDifficultyButtonAccessible(currentButton, currentDifficulty)
            }
        }
    }

    private fun setDifficultyButtonNotAccessible(currentButton: Button) {
        currentButton.setBackgroundResource(R.drawable.level_locked)
        currentButton.setTextColor(ContextCompat.getColor(this, R.color.medium_color))
    }

    private fun setDifficultyButtonAccessible(currentButton: Button, currentDifficulty: Int) {
        currentButton.setBackgroundResource(R.drawable.level_unlocked)
        currentButton.setTextColor(ContextCompat.getColor(this, R.color.light_color))

        // add listener
        currentButton.setOnClickListener {
            goToLevelSelection(currentDifficulty)
        }
    }

    private fun initializePage() {

        findViewById<Button>(R.id.button_back).setOnClickListener { finish() }

        for (difficulty in 0 until Config.NUMBER_OF_DIFFICULTIES) {
            createDifficultyButtons(findViewById(R.id.group_levels), difficulty)
        }
    }
}

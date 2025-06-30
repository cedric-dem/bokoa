package com.slykos.bokoa.pagesHandler

import android.content.Intent
import android.os.Bundle
import android.util.TypedValue
import android.widget.Button
import android.widget.LinearLayout
import android.widget.Space
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.slykos.bokoa.R
import com.slykos.bokoa.models.SavedDataHandler

class DifficultySelectionPageHandler : AppCompatActivity() {
    private var levelsPerDifficulty: Int = 0
    private var numberOfDifficulty: Int = 0
    private var difficultyNames: Array<String> = arrayOf()

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

    private fun createDifficultyButtons(groupLvl: LinearLayout, difficulty: Int) {
        val newButton = Button(this)

        newButton.id = 2000 + difficulty
        newButton.setTextColor(ContextCompat.getColor(this, R.color.light_color))

        newButton.text = difficultyNames[difficulty]

        newButton.setTextSize(TypedValue.COMPLEX_UNIT_SP, 23f)

        newButton.typeface = resources.getFont(R.font.main_font)

        groupLvl.addView(newButton, getWeightLayoutParameter())

        val tempSpace = Space(this)
        tempSpace.minimumHeight = 30
        groupLvl.addView(tempSpace)
    }

    private fun goToLevelSelection(difficulty: Int) {
        val switchActivityIntent = Intent(applicationContext, LevelSelectionPageHandler::class.java)

        switchActivityIntent.putExtra("difficulty", difficulty)

        startActivity(switchActivityIntent)
    }

    private fun configureDifficultyButtons() {
        val passedLevels = savedDataHandler.getPassedLevels()

        var currentButton: Button

        for (currentDifficulty in 0 until numberOfDifficulty) { // difficulty

            currentButton = findViewById(2000 + currentDifficulty)

            if (passedLevels < (levelsPerDifficulty * currentDifficulty)) { // Not accessible
                currentButton.setBackgroundResource(R.drawable.level_locked)
                currentButton.setTextColor(ContextCompat.getColor(this, R.color.medium_color))
            } else { // accessible
                currentButton.setBackgroundResource(R.drawable.level_unlocked)
                currentButton.setTextColor(ContextCompat.getColor(this, R.color.light_color))

                // add listener
                val tmpCurrentDifficulty = currentDifficulty
                currentButton.setOnClickListener {
                    goToLevelSelection(
                        tmpCurrentDifficulty
                    )
                }
            }
        }
    }

    private fun initializePage() {
        difficultyNames = resources.getStringArray(R.array.difficulty_names)
        levelsPerDifficulty = resources.getInteger(R.integer.levels_per_difficulty)
        numberOfDifficulty = resources.getInteger(R.integer.number_of_difficulty)

        findViewById<Button>(R.id.button_back).setOnClickListener { finish() }

        for (difficulty in 0 until numberOfDifficulty) {
            createDifficultyButtons(
                findViewById(R.id.group_levels),
                difficulty
            )
        }
    }
}

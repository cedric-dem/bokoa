package com.slykos.bokoa.frontend.pages

import android.content.Intent
import android.os.Bundle
import android.util.TypedValue
import android.widget.Button
import android.widget.LinearLayout
import android.widget.Space
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.lifecycle.ViewModelProvider
import com.slykos.bokoa.R
import com.slykos.bokoa.config.Config
import com.slykos.bokoa.data.user.SavedDataHandler
import com.slykos.bokoa.data.user.UserRepository
import com.slykos.bokoa.frontend.viewmodels.viewmodel.DifficultySelectionViewModel
import com.slykos.bokoa.frontend.viewmodels.viewmodelfactory.DifficultySelectionViewModelFactory

class DifficultySelectionPageHandler : AppCompatActivity() {

    private lateinit var viewModel: DifficultySelectionViewModel

    public override fun onResume() {
        super.onResume()
        // TODO set difficulty
        viewModel.loadDifficultyStates()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_difficulty_selection)

        val userRepository: UserRepository = SavedDataHandler(this)
        viewModel = ViewModelProvider(
            this,
            DifficultySelectionViewModelFactory(userRepository)
        )[DifficultySelectionViewModel::class.java]

        initializePage()

        observeViewModel()
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
        val switchActivityIntent = Intent(this, LevelSelectionPageHandler::class.java)

        switchActivityIntent.putExtra("difficulty", difficulty)

        startActivity(switchActivityIntent)
    }

    private fun observeViewModel() {
        viewModel.difficultyStates.observe(this) { states ->
            configureDifficultyButtons(states)
        }
    }

    private fun configureDifficultyButtons(states: List<DifficultySelectionViewModel.DifficultyState>) {
        var currentButton: Button
        for (state in states) {
            currentButton = findViewById(2000 + state.difficulty)
            if (state.accessible) {
                setDifficultyButtonAccessible(currentButton, state.difficulty)
            } else {
                setDifficultyButtonNotAccessible(currentButton)
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

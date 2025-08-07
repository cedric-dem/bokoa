package com.slykos.bokoa.frontend.pages

import android.content.Intent
import android.os.Bundle
import android.view.Gravity
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.gridlayout.widget.GridLayout
import androidx.lifecycle.ViewModelProvider
import com.slykos.bokoa.R
import com.slykos.bokoa.config.Config
import com.slykos.bokoa.data.user.SavedDataHandler
import com.slykos.bokoa.data.user.UserRepository
import com.slykos.bokoa.frontend.pages.playPages.GamePageHandler
import com.slykos.bokoa.frontend.viewmodels.viewmodel.LevelSelectionViewModel
import com.slykos.bokoa.frontend.viewmodels.viewmodelfactory.LevelSelectionViewModelFactory

class LevelSelectionPageHandler : AppCompatActivity() {
    private var textSize: Int = 0

    private var marginSize: Int = 0
    private var caseHeight: Int = 0
    private var caseWidth: Int = 0

    private lateinit var viewModel: LevelSelectionViewModel

    private var difficulty: Int = 0

    public override fun onResume() {
        super.onResume()
        viewModel.loadLevelStates(difficulty)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_level_selection)

        val userRepository: UserRepository = SavedDataHandler(this)
        viewModel = ViewModelProvider(
            this,
            LevelSelectionViewModelFactory(userRepository)
        )[LevelSelectionViewModel::class.java]

        initializeMetrics()

        getExtra()

        initializePage()

        observeViewModel()
    }

    private fun createButton(groupLvl: GridLayout, row: Int, col: Int) {
        val levelId = (Config.LEVELS_PER_DIFFICULTIES * difficulty) + (Config.LEVELS_SELECTION_COLUMNS * row) + col

        val newButton = Button(this).apply {
            id = 2000 + levelId
            gravity = Gravity.CENTER
            typeface = resources.getFont(R.font.main_font)
            textSize = this@LevelSelectionPageHandler.textSize.toFloat()
            text = (levelId + 1).toString()
        }

        groupLvl.addView(newButton, getGridParams(row, col))
    }

    private fun observeViewModel() {
        viewModel.levelStates.observe(this) { states ->
            configureLevelButtons(states)
        }
    }

    private fun configureLevelButtons(states: List<LevelSelectionViewModel.LevelState>) {
        var currentButton: Button
        for (state in states) {
            val buttonId = 2000 + difficulty * Config.LEVELS_PER_DIFFICULTIES + state.level
            currentButton = findViewById(buttonId)
            if (state.accessible) {
                currentButton.setTextColor(ContextCompat.getColor(this, R.color.light_color))
                currentButton.setBackgroundResource(R.drawable.level_unlocked)
                currentButton.setOnClickListener { launchGame(state.level) }
            } else {
                currentButton.setBackgroundResource(R.drawable.level_locked)
                currentButton.setTextColor(ContextCompat.getColor(this, R.color.medium_color))
            }
        }
    }

    private fun getGridParams(i: Int, j: Int): GridLayout.LayoutParams = //TODO remove code duplication
        GridLayout.LayoutParams().apply {
            setMargins(marginSize, marginSize, marginSize, marginSize)
            height = caseHeight
            width = caseWidth
            rowSpec = GridLayout.spec(i)
            columnSpec = GridLayout.spec(j)
        }

    private fun launchGame(levelId: Int) {
        val switchActivityIntent = Intent(applicationContext, GamePageHandler::class.java)

        switchActivityIntent.putExtra("level", levelId)
        switchActivityIntent.putExtra("difficulty", difficulty)

        startActivity(switchActivityIntent)
    }

    private fun initializeMetrics() {

        val displayMetrics = this@LevelSelectionPageHandler.resources.displayMetrics

        caseWidth = ((displayMetrics.widthPixels * 0.87) / Config.LEVELS_SELECTION_COLUMNS).toInt()

        caseHeight = ((displayMetrics.heightPixels * (0.0148 * Config.LEVELS_PER_DIFFICULTIES)) / Config.LEVELS_SELECTION_ROWS).toInt()

        marginSize = displayMetrics.widthPixels / 154
        textSize = displayMetrics.widthPixels / 45
    }

    private fun configureTopBar() {
        findViewById<TextView>(R.id.page_title).text = getString(R.string.level_selection_menu) + getString(R.string.difficulty) + ": " + Config.DIFFICULTIES_NAMES[difficulty]

        findViewById<Button>(R.id.button_back).setOnClickListener { finish() }
    }

    private fun initializeLevelPanel() {
        val groupLvl = findViewById<GridLayout>(R.id.group_levels)

        for (currentRow in 0 until Config.LEVELS_SELECTION_ROWS) {
            for (currentCol in 0 until Config.LEVELS_SELECTION_COLUMNS) {
                createButton(groupLvl, currentRow, currentCol)
            }
        }
    }

    private fun initializePage() {
        configureTopBar()

        initializeLevelPanel()
    }

    private fun getExtra() {
        difficulty = intent.extras!!.getInt("difficulty")
    }
}

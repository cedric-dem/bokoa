package com.slykos.bokoa.pagesHandler

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.view.Gravity
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.gridlayout.widget.GridLayout
import com.slykos.bokoa.R
import com.slykos.bokoa.models.SavedDataHandler

class LevelSelectionPageHandler : AppCompatActivity() {
    private var levelsPerDifficulty: Int = 0
    private var rowCount: Int = 0
    private var colCount: Int = 0
    private var textSize: Int = 0

    private var marginSize: Int = 0
    private var caseHeight: Int = 0
    private var caseWidth: Int = 0
    private var levelsSectionsNames: Array<String> = arrayOf()
    private lateinit var savedDataHandler: SavedDataHandler

    private var difficulty: Int = 0

    public override fun onResume() {
        super.onResume()
        configureButtonsLevels()
    }

    @SuppressLint("SetTextI18n")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_level_selection)

        savedDataHandler = SavedDataHandler(this)

        initializeMetrics()

        getExtra()

        initializePage()
        // configure called by onResume
    }

    @SuppressLint("SetTextI18n")
    private fun createButton(groupLvl: GridLayout, row: Int, col: Int) {
        val newButton = Button(this)

        val lvlId = (levelsPerDifficulty * difficulty) + (colCount * row) + col
        newButton.id = 2000 + lvlId
        newButton.gravity = Gravity.CENTER

        newButton.typeface = resources.getFont(R.font.main_font)

        newButton.textSize = textSize.toFloat()

        newButton.text = (lvlId + 1).toString()

        groupLvl.addView(newButton, getGridParams(row, col))
    }

    private fun configureButtonsLevels() {
        val passedLevels = savedDataHandler.getPassedLevels()

        var currentButton: Button

        for (currentLevel in 0 until levelsPerDifficulty) { // levels
            currentButton = findViewById(2000 + difficulty * levelsPerDifficulty + currentLevel)

            if (passedLevels < (levelsPerDifficulty * difficulty) + currentLevel) { // Not accessible
                currentButton.setBackgroundResource(R.drawable.level_locked)
                currentButton.setTextColor(ContextCompat.getColor(this, R.color.medium_color))
            } else { // accessible

                currentButton.setTextColor(ContextCompat.getColor(this, R.color.light_color))
                currentButton.setBackgroundResource(R.drawable.level_unlocked)

                // add listener
                currentButton.setOnClickListener {
                    launchGame(
                        currentLevel
                    )
                }
            }
        }
    }

    private fun getGridParams(i: Int, j: Int): GridLayout.LayoutParams {
        // TODO remove code duplication

        val params = GridLayout.LayoutParams()

        params.rightMargin = marginSize
        params.leftMargin = marginSize
        params.topMargin = marginSize
        params.bottomMargin = marginSize

        params.height = caseHeight
        params.width = caseWidth

        params.rowSpec = GridLayout.spec(i)
        params.columnSpec = GridLayout.spec(j)

        return params
    }

    private fun launchGame(levelId: Int) {
        val switchActivityIntent = Intent(applicationContext, GamePageHandler::class.java)

        switchActivityIntent.putExtra("level", levelId)
        switchActivityIntent.putExtra("difficulty", difficulty)

        startActivity(switchActivityIntent)
    }

    private fun initializeMetrics() {
        levelsSectionsNames = resources.getStringArray(R.array.difficulty_names)
        levelsPerDifficulty = resources.getInteger(R.integer.levels_per_difficulty)

        rowCount = resources.getInteger(R.integer.levels_selection_rows)
        colCount = resources.getInteger(R.integer.levels_selection_cols)

        val displayMetrics = this@LevelSelectionPageHandler.resources.displayMetrics

        caseWidth = ((displayMetrics.widthPixels * 0.87) / colCount).toInt()

        caseHeight =
            ((displayMetrics.heightPixels * (0.0148 * levelsPerDifficulty)) / rowCount).toInt()

        marginSize = displayMetrics.widthPixels / 154
        textSize = displayMetrics.widthPixels / 45
    }

    @SuppressLint("SetTextI18n")
    private fun configureTopBar() {
        findViewById<TextView>(R.id.page_title).text =
            getString(R.string.level_selection_menu) + getString(R.string.difficulty) + ": " + levelsSectionsNames[difficulty]

        findViewById<Button>(R.id.button_back).setOnClickListener { finish() }
    }

    private fun initializeLevelPanel() {
        val groupLvl = findViewById<GridLayout>(R.id.group_levels)

        for (currentRow in 0 until rowCount) {
            for (currentCol in 0 until colCount) {
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

package com.slykos.bokoa

import android.content.Context
import android.content.Intent
import androidx.test.core.app.ActivityScenario
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import com.slykos.bokoa.config.Config
import com.slykos.bokoa.frontend.pages.playPages.GamePageHandler
import org.junit.Test
import org.junit.runner.RunWith
import kotlin.test.assertEquals
import kotlin.test.assertTrue
import kotlin.test.assertFalse

@RunWith(AndroidJUnit4::class)
class GameInstrumentedTest {

    private fun getScenario(levelId: Int, difficulty: Int): ActivityScenario<GamePageHandler>? {
        val context = ApplicationProvider.getApplicationContext<Context>()
        val intent = Intent(context, GamePageHandler::class.java).apply {
            putExtra("level", levelId)
            putExtra("difficulty", difficulty)
        }
        return ActivityScenario.launch(intent)
    }

    @Test
    fun testAllLevelsSolutions() {
        getScenario(0, 0)?.onActivity { activity ->
            for (currentLevelIndex in 0 until Config.NUMBER_OF_DIFFICULTIES * Config.LEVELS_PER_DIFFICULTIES - 1) {
                assertFalse(activity.checkGoalReached())
                activity.solve()
                assertTrue(activity.checkGoalReached())
                activity.nextLevel()
            }
        }
    }

    @Test
    fun testNonEffectiveMove() {
        for (currentDifficultyIndex in 0 until Config.NUMBER_OF_DIFFICULTIES) {
            getScenario(12, currentDifficultyIndex)?.onActivity { activity ->
                activity.getGame().moveLeft()
                activity.getGame().moveUp()

                assertEquals(
                    1.0,
                    activity.getGame().getCurrentScore()
                )

                assertEquals(
                    1,
                    activity.getGame().getMoveHandler().getHistorySize()
                )

                activity.getGame().moveRight()
                activity.getGame().moveDown()

                assertEquals(
                    3,
                    activity.getGame().getMoveHandler().getHistorySize()
                )

            }
        }
    }
}
package com.slykos.bokoa

import android.content.Context
import androidx.test.core.app.ApplicationProvider
import com.slykos.bokoa.data.levels.loadLevelFromJson
import com.slykos.bokoa.logic.models.Operation
import kotlin.test.assertEquals
import kotlin.test.assertNotNull
import kotlin.test.assertNull
import org.junit.Test

class LevelLoaderTest {
    private val context: Context = ApplicationProvider.getApplicationContext()

    @Test
    fun loadValidLevel() {
        val level = loadLevelFromJson(context, "test/level_000000.json")
        assertNotNull(level)
        assertEquals(50.0, level.bestScore)
        assertEquals(listOf(">", "u", ">", "u"), level.bestMoves.toList())
        assertEquals(
            Operation(true, null, null),
            level.operations[0][0]
        )
        assertEquals(
            Operation(false, '+', 3f),
            level.operations[0][1]
        )
    }

    @Test
    fun loadMissingLevelReturnsNull() {
        val level = loadLevelFromJson(context, "missing.json")
        assertNull(level)
    }
}
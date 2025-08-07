package com.slykos.bokoa

import com.slykos.bokoa.logic.models.Operation
import kotlin.test.assertEquals
import org.junit.Test

class OperationTest {

    @Test
    fun applyAddition() {
        val op = Operation(false, '+', 3f)
        assertEquals(13.0, op.applyOperation(10.0, false))
        assertEquals(7.0, op.applyOperation(10.0, true))
    }

    @Test
    fun applySubtraction() {
        val operation = Operation(false, '-', 3f)
        assertEquals(7.0, operation.applyOperation(10.0, false))
        assertEquals(13.0, operation.applyOperation(10.0, true))
    }

    @Test
    fun applyMultiplication() {
        val op = Operation(false, '×', 2f)
        assertEquals(20.0, op.applyOperation(10.0, false))
        assertEquals(5.0, op.applyOperation(10.0, true))
    }

    @Test
    fun applyDivision() {
        val operation = Operation(false, '÷', 2f)
        assertEquals(5.0, operation.applyOperation(10.0, false))
        assertEquals(20.0, operation.applyOperation(10.0, true))
    }

    @Test
    fun applyNeutral() {
        val operation = Operation(true, null, null)
        assertEquals(10.0, operation.applyOperation(10.0, false))
    }
}

package com.slykos.bokoa.models

data class Operation(
    val isNeutral: Boolean,
    val operator: Char?,
    val operand: Int?
) {
    companion object {
        //todo add bool isneutral
        //todo add class + - / * inheritingf from that, apply() function
        fun fromString(s: String): Operation {
            if (s.length != 1) {
                return Operation(false, s[0], s.substring(1).toInt())
            } else {
                return Operation(true, null, null)
            }
        }
    }

    val asString: String
        get() = if (isNeutral) "1" else "$operator$operand"

    fun applyOperation(inputValue: Float, reverse: Boolean): Float {
        val op = operator ?: return inputValue
        val value = operand ?: return inputValue

        return when (op) {
            '+' -> inputValue + if (reverse) -value else value
            '-' -> inputValue + if (reverse) value else -value
            '×' -> inputValue * if (reverse) 1 / value else value
            '÷' -> inputValue * if (reverse) value else 1 / value
            else -> inputValue
        }
    }
}
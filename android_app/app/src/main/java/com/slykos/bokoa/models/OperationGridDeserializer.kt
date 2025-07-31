package com.slykos.bokoa.models

import com.google.gson.JsonDeserializationContext
import com.google.gson.JsonDeserializer
import com.google.gson.JsonElement

import java.lang.reflect.Type

class OperationGridDeserializer : JsonDeserializer<Array<Array<Operation>>> {
    override fun deserialize(
        json: JsonElement,
        typeOfT: Type,
        context: JsonDeserializationContext
    ): Array<Array<Operation>> {
        val jsonArray = json.asJsonArray

        return jsonArray.map { inner ->
            inner.asJsonArray.map { element ->
                Operation.fromString(element.asString)
            }.toTypedArray()
        }.toTypedArray()
    }
}
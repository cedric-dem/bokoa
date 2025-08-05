package com.slykos.bokoa.data.levels

import android.content.Context
import com.google.gson.GsonBuilder
import com.slykos.bokoa.logic.models.Level
import com.slykos.bokoa.logic.models.Operation
import java.io.InputStreamReader

fun loadLevelFromJson(context: Context, filename: String): Level? =
    try {
        val reader = InputStreamReader(context.assets.open(filename))

        val gson = GsonBuilder()
            .registerTypeAdapter(
                Array<Array<Operation>>::class.java,
                OperationGridDeserializer()
            )
            .create()

        gson.fromJson(reader, Level::class.java).also {
            reader.close()
        }
    } catch (e: Exception) {
        e.printStackTrace()
        null
    }
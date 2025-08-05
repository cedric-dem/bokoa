package com.slykos.bokoa.frontend.pages

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import com.slykos.bokoa.R
import com.slykos.bokoa.frontend.pages.playPages.TutorialPageHandler

class HowToPlayPageHandler : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_how_to_play)

        initializePage()
    }

    private fun initializePage() {
        findViewById<Button>(R.id.button_back).setOnClickListener { finish() }

        findViewById<Button>(R.id.button_tutorial).setOnClickListener {
            startActivity(
                Intent(
                    applicationContext,
                    TutorialPageHandler::class.java
                )
            )
        }
    }
}

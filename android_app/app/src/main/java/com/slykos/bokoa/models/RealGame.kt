package com.slykos.bokoa.models

import android.annotation.SuppressLint
import com.slykos.bokoa.pagesHandler.GamePageHandler

class RealGame(
    private var callingPage: GamePageHandler
) :
    Game(
        callingPage
    ) {

    @SuppressLint("SetTextI18n")
    override fun refreshScore() {
        super.refreshScore()
        callingPage.setScoreText(
            """${getGoodFormat(currentScore)} / $bestScoreStr"""
        )
    }
}

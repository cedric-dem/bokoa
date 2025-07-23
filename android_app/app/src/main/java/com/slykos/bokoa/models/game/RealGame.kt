package com.slykos.bokoa.models.game

import com.slykos.bokoa.pagesHandler.GamePageHandler

class RealGame(
    private var callingPage: GamePageHandler
) :
    Game(
        callingPage
    ) {

    override fun refreshScore() {
        super.refreshScore()
        callingPage.setScoreText("""${getFormattedScore(currentScore)} / $bestScoreStr""")
    }
}

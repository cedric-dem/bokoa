package com.slykos.bokoa.logic.game

import com.slykos.bokoa.frontend.pages.playPages.GamePageHandler

class RealGame(
    private var callingPage: GamePageHandler
) :
    Game(
        callingPage
    ) {

    override fun refreshScore() {
        super.refreshScore()
        callingPage.setScoreText("""${getFormattedScore(currentScore)} / $bestScoreString""")
    }
}

package com.slykos.bokoa.logic.game

import com.slykos.bokoa.frontend.pages.playPages.GenericPlayPage

class RealGame(
    context: GenericPlayPage,
    private val onScoreChanged: (String) -> Unit,
) :
    Game(
        context
    ) {

    override fun refreshScore() {
        super.refreshScore()
        onScoreChanged("""${getFormattedScore(getCurrentScore())} / ${getBestScoreString()}""")
    }
}
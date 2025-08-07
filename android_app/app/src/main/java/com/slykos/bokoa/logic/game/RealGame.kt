package com.slykos.bokoa.logic.game

import com.slykos.bokoa.logic.game.GameUi

class RealGame(
    ui: GameUi,
    private val onScoreChanged: (String) -> Unit,
) :
    Game(
        ui
    ) {

    override fun refreshScore() {
        super.refreshScore()
        onScoreChanged("""${getFormattedScore(getCurrentScore())} / ${getBestScoreString()}""")
    }
}
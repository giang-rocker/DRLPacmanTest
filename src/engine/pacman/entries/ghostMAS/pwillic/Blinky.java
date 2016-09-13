package engine.pacman.entries.ghostMAS.pwillic;

import engine.pacman.controllers.IndividualGhostController;
import engine.pacman.game.Constants;
import engine.pacman.game.Game;

/**
 * Created by Piers on 11/11/2015.
 */
public class Blinky extends IndividualGhostController {

    private POCommGhost ghost;

    public Blinky() {
        super(Constants.GHOST.BLINKY);
        ghost = new POCommGhost(Constants.GHOST.BLINKY, 50);
    }

    @Override
    public Constants.MOVE getMove(Game game, long timeDue) {
        return ghost.getMove(game, timeDue);
    }
}

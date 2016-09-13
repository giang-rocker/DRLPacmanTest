package engine.pacman.entries.ghostMAS;

import engine.pacman.controllers.IndividualGhostController;
import engine.pacman.game.Constants;
import engine.pacman.game.Game;

/**
 * Created by Piers on 11/11/2015.
 */
public class Sue extends IndividualGhostController {

    public Sue() {
        super(Constants.GHOST.SUE);
    }

    @Override
    public Constants.MOVE getMove(Game game, long timeDue) {
        return null;
    }
}

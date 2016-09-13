package engine.pacman.entries.ghostMAS;

import engine.pacman.controllers.IndividualGhostController;
import engine.pacman.game.Constants;
import engine.pacman.game.Game;

/**
 * Created by Piers on 11/11/2015.
 */
public class Pinky extends IndividualGhostController {

    public Pinky() {
        super(Constants.GHOST.PINKY);
    }

    @Override
    public Constants.MOVE getMove(Game game, long timeDue) {
        return null;
    }
}

package engine.pacman.entries.ghostMAS.pwillic;

import engine.pacman.controllers.IndividualGhostController;
import engine.pacman.game.Constants;
import engine.pacman.game.Game;

/**
 * Created by Piers on 11/11/2015.
 */
public class Pinky extends IndividualGhostController {
    private POCommGhost ghost;

    public Pinky() {
        super(Constants.GHOST.PINKY);
        ghost = new POCommGhost(Constants.GHOST.PINKY, 50);
    }

    @Override
    public Constants.MOVE getMove(Game game, long timeDue) {
        return ghost.getMove(game, timeDue);
    }
}

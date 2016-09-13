package engine.pacman.controllers.examples;

import engine.pacman.controllers.PacmanController;
import engine.pacman.game.Constants.MOVE;
import engine.pacman.game.Game;

import java.util.Random;


/*
 * The Class RandomNonRevPacMan.
 */
public final class RandomNonRevPacMan extends PacmanController {
    Random rnd = new Random();

    /* (non-Javadoc)
     * @see pacman.controllers.Controller#getMove(pacman.game.Game, long)
     */
    public MOVE getMove(Game game, long timeDue) {
        MOVE[] possibleMoves = game.getPossibleMoves(game.getPacmanCurrentNodeIndex(), game.getPacmanLastMoveMade());        //set flag as false to prevent reversals

        return possibleMoves[rnd.nextInt(possibleMoves.length)];
    }
}
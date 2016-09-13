package engine.pacman.controllers.examples;

import engine.pacman.controllers.PacmanController;
import engine.pacman.game.Constants.MOVE;
import engine.pacman.game.Game;

import java.util.Random;

/*
 * The Class RandomPacMan.
 */
public final class RandomPacMan extends PacmanController {
    private Random rnd = new Random();
    private MOVE[] allMoves = MOVE.values();

    /* (non-Javadoc)
     * @see pacman.controllers.Controller#getMove(pacman.game.Game, long)
     */
    public MOVE getMove(Game game, long timeDue) {
        return allMoves[rnd.nextInt(allMoves.length)];
    }
}
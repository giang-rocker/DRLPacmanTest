package engine.pacman.test;

import engine.pacman.game.Constants.GHOST;
import engine.pacman.game.Constants.MOVE;
import engine.pacman.game.Game;
import engine.pacman.game.comms.BasicMessenger;
import engine.pacman.game.info.GameInfo;
import engine.pacman.game.internal.Ghost;
import engine.pacman.game.internal.PacMan;

import java.util.EnumMap;


/**
 * Created by pwillic on 09/05/2016.
 */
public class ForwardModelTest {

    public static void main(String[] args) {

        Game game = new Game(System.currentTimeMillis(), new BasicMessenger(0, 1, 1));

        game.copy(new PacMan(game.getPacmanCurrentNodeIndex(), MOVE.DOWN, 2, true));

        GameInfo info = game.getBlankGameInfo();
        // Just forward the game itself

        info.setPacman(new PacMan(game.getPacmanCurrentNodeIndex(), MOVE.DOWN, game.getPacmanNumberOfLivesRemaining(), true));
        info.setGhostIndex(GHOST.INKY, new Ghost(GHOST.INKY, 10, 0, 0, MOVE.NEUTRAL));

        Game next = game.getGameFromInfo(info);
        for (int i = 0; i < 100; i++) {
            EnumMap<GHOST, MOVE> inkyMove = new EnumMap<>(GHOST.class);
            inkyMove.put(GHOST.INKY, MOVE.LEFT);
            next.advanceGame(MOVE.DOWN, inkyMove);
            System.out.println(next.getGhostCurrentNodeIndex(GHOST.INKY));
        }

        System.out.println("Finished");

    }
}

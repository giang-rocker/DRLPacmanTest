package engine.pacman.controllers.examples;

import engine.pacman.controllers.Controller;
import engine.pacman.game.Constants.GHOST;
import engine.pacman.game.Constants.MOVE;
import engine.pacman.game.Game;

import java.util.EnumMap;

/**
 * Created by pwillic on 09/06/2016.
 */
public class DudGhosts extends Controller<EnumMap<GHOST, MOVE>> {

    @Override
    public EnumMap<GHOST, MOVE> getMove(Game game, long timeDue) {
        return null;
    }
}

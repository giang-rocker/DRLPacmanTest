package engine.pacman.test;

import engine.pacman.Executor;
import engine.pacman.controllers.HumanController;
import engine.pacman.controllers.KeyBoardInput;
import engine.pacman.controllers.PacmanController;
import engine.pacman.controllers.examples.po.POCommGhosts;
import engine.pacman.controllers.examples.po.POPacMan;
import engine.pacman.game.Constants;
import engine.pacman.game.Game;
import engine.pacman.game.GameView;
import engine.pacman.game.comms.BasicMessenger;
import engine.pacman.game.internal.POType;

import java.util.EnumMap;

/**
 * Created by Piers on 22/06/2016.
 */
public class HumanTest {

    public static void main(String[] args) {
        Executor executor = new Executor(true, true);

        KeyBoardInput input = new KeyBoardInput();

        Game primaryGame = new Game(0);

        GameView view  = new GameView(primaryGame).showGame();
        GameView radiusView = new GameView(primaryGame).showGame();
        GameView ff_losView = new GameView(primaryGame).showGame();

        view.setPO(true);
        radiusView.setPO(true);
        ff_losView.setPO(true);

        HumanController human = new HumanController(input);
        PacmanController pacman = new POPacMan();
        POCommGhosts ghosts = new POCommGhosts(50);

        view.setFocusable(true);
        view.requestFocus();
        view.addKeyListener(human.getKeyboardInput());

        while(!primaryGame.gameOver()){
            try{
                Thread.sleep(40);
            } catch (Exception e){

            }
            primaryGame.PO_TYPE = POType.LOS;
            primaryGame.SIGHT_LIMIT = 100;

            Constants.MOVE pacmanMove = pacman.getMove(primaryGame.copy(5), 40);
            EnumMap<Constants.GHOST, Constants.MOVE> ghostMoves = ghosts.getMove(primaryGame.copy(), -1);

            primaryGame.advanceGame(pacmanMove, ghostMoves);


            //radiusGame.advanceGame(pacmanMove, ghostMoves);
            //ff_losGame.advanceGame(pacmanMove, ghostMoves);

            view.paintImmediately(view.getBounds());
            primaryGame.PO_TYPE = POType.RADIUS;
            primaryGame.SIGHT_LIMIT = 45;
            radiusView.paintImmediately(radiusView.getBounds());
            primaryGame.PO_TYPE = POType.FF_LOS;
            primaryGame.SIGHT_LIMIT = 100;
            ff_losView.paintImmediately(ff_losView.getBounds());
        }
        System.out.println("Ended");
    }
}

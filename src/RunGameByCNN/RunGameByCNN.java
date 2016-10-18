/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package RunGameByCNN;

import engine.pacman.game.Constants;
import engine.pacman.game.Constants.MOVE;
import engine.pacman.game.Game;
import java.util.EnumMap;

/**
 *
 * @author giang-rocker
 */
public class RunGameByCNN {
    
     public static void main(String[] args){
          
         String command = args[0];
         if (command.equals("START_GAME")){
            Game game = new Game(0);
            System.out.println(game.getGameState());
         }
         else if (command.equals("RUN_GAME")) {
             String gameState = args[1];             
             Game game = new Game(0);
             game.setGameState(gameState);
             
            int action = Integer.parseInt(args[2]);
            MOVE nextMove = MOVE.NEUTRAL;
            // UP RIGHT DOWN LEFT NEUTRAL
            switch(action) {
                case 0: nextMove = MOVE.UP ; break;
                case 1: nextMove = MOVE.RIGHT ; break;
                case 2: nextMove = MOVE.DOWN ; break;
                case 3: nextMove = MOVE.LEFT ; break;
                case 4: nextMove = MOVE.NEUTRAL ; break;
            
            }
            
            testFull.SimulateGhostMove ghostsMove = new testFull.SimulateGhostMove();
            EnumMap<Constants.GHOST, MOVE> listGhostMove = new EnumMap<>(Constants.GHOST.class);
            //STRATEGY MOVE
            Game simulatedGame = game.copy(false);
            listGhostMove = ghostsMove.getMove(simulatedGame);
             
             
             game.advanceGame(nextMove, listGhostMove);
             if (game.gameOver())
                System.out.println("GAME_OVER");
             else
                System.out.println(game.getGameState());
         
         }
        
    }
    
}

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package DRL;

import engine.pacman.Executor;
import engine.pacman.controllers.PacmanController;
import engine.pacman.game.Constants;
import engine.pacman.game.Constants.MOVE;
import engine.pacman.game.Game;
import examples.commGhosts.POCommGhosts;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.util.Random;
import testFull.MyPacMan;

/**
 *
 * @author giang-rocker
 */
public class LearningPacMan  extends PacmanController {

    @Override
    public Constants.MOVE getMove(Game game, long timeDue) {
          Random R = new Random();
        int nextInt  = R.nextInt(4);
       // System.out.println("SEND FROM JAVA " + nextInt);
        int ret =0 ;
        try{
            String gameState = game.getGameState();
            Process p = Runtime.getRuntime().exec("python3 getState.py " + nextInt);
            BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
            ret = new Integer(in.readLine()).intValue();
            //System.out.println("value return from Python : "+ret);
            }catch(Exception e){
            System.out.println(e.getMessage());
            }
        
        if (ret == nextInt) System.out.println("TRUE");
        else System.out.println("FALSE");
        
       MOVE nextMove = MOVE.NEUTRAL;
        switch(ret){
            case 0: nextMove = MOVE.DOWN; break;
            case 1: nextMove = MOVE.LEFT; break;
            case 2: nextMove = MOVE.UP; break;
            case 3: nextMove = MOVE.RIGHT; break;
            case 4: nextMove = MOVE.NEUTRAL; break;
        }
        
        
        
        return nextMove;
    }

    public static void main(String[] args){
        
        Executor ex = new Executor(true, true);
        ex.runGameTimed(new LearningPacMan(), new POCommGhosts(50), true);
        
    }
}



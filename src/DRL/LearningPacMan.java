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
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;
import testFull.MyPacMan;

/**
 *
 * @author giang-rocker
 */
public class LearningPacMan  extends PacmanController {
    Process p ;
    public LearningPacMan() {
       // System.out.println("SEND FROM JAVA " + nextInt);
        try{
            p= Runtime.getRuntime().exec("python3 .py");
            }catch(Exception e){
            System.out.println(e.getMessage());
            }
        
    
    }
    
    @Override
    public Constants.MOVE getMove(Game game, long timeDue) {
        
        BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
        int ret=0;
        try {
            ret = new Integer(in.readLine()).intValue();
        } catch (IOException ex) {
            Logger.getLogger(LearningPacMan.class.getName()).log(Level.SEVERE, null, ex);
        }
       
      
      
        
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



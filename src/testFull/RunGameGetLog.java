/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package testFull;

import engine.pacman.Executor;
import examples.commGhosts.POCommGhosts;

/**
 *
 * @author Giang
 */
public class RunGameGetLog {
    
    public static void main(String[] args){
        int numOfGame = 1000;
        Executor ex = new Executor(true, true);
       
        for (int i =0; i < numOfGame;i++){
        ex.runGameTimedRecorded(new MyPacMan(), new POCommGhosts(50), true,("F"+i+".txt"));
        }
    //ex.runGame(new HumanController(new KeyBoardInput()), new POCommGhosts(50), true, 40);
    }
    
}

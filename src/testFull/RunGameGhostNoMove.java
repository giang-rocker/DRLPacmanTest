/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package testFull;

import engine.pacman.Executor;
import examples.commGhosts.POCommGhosts;
import examples.poPacMan.POPacMan;

/**
 *
 * @author Giang
 */
public class RunGameGhostNoMove {
    
    public static void main(String[] args){
        Executor ex = new Executor(false, false);
       
        
        ex.runGameGhostNoMove(new POPacMan(),true);
      
    }
    
}

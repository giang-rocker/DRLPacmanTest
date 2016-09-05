/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package extractorpacman;

import examples.commGhosts.POCommGhosts;
import examples.poPacMan.POPacMan;
import pacman.Executor;
import pacman.game.Game;

/**
 *
 * @author giang-rocker
 */
public class MainTest {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        
          Executor executor = new Executor(true, true);

        executor.runGameTimed(new POPacMan(), new POCommGhosts(50), true);
        
        
    }
    
}

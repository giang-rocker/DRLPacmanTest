/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package extractorpacman;

import examples.commGhosts.POCommGhosts;
import examples.poPacMan.POPacMan;
import static javafx.scene.input.KeyCode.X;
import engine.pacman.Executor;
import engine.pacman.game.Game;
import engine.pacman.game.internal.Node;

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
       
        for (int i =0; i < 4; i++){
       Game  X = new Game(0, i);
       int maxX =0; int maxY = 0;
       for (Node node : X.getCurrentMaze().graph){
           int id = node.nodeIndex;
           int x = X.getNodeXCood(id);
           int y = X.getNodeYCood(id);
     //      System.out.println("node " + id + " at position (" + x +" ; " + y  +")");
           if (x>maxX) maxX = x;
           if (y>maxY) maxY = y;
       }
       
        System.out.println("SIZE of MAZE : " +i +" " +maxX +"x"+maxY + " with " + X.getCurrentMaze().graph.length +" nodes" );
        }
        
        
        
        
    }
    
}

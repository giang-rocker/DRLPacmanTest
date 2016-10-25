/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package extractorpacman.extractorPython;

import engine.pacman.Executor;
import examples.commGhosts.POCommGhosts;
import java.io.File;
import testFull.MyPacMan;

/**
 *
 * @author giang-rocker
 */
public class RunGameLogFile {
    
      public static void main(String[] args){
        int numOfGame = 1000;
        
        File logFile=new File("src/extractorpacman/extractorPython/logGameCNN.txt");
        System.out.println(logFile.getAbsolutePath());
        System.out.println(logFile.exists());
        
        Executor ex = new Executor(true, true);
        ex.replayGame(logFile.getAbsolutePath(), true);
    }
    
}

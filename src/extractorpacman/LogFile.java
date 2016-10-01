
/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package extractorpacman;

import static engine.pacman.game.Constants.pathMazes;
import engine.pacman.game.internal.Node;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.LineNumberReader;
import java.util.Scanner;

/**
 *
 * @author giang-rocker
 */
public class LogFile {

    String fileName;
    int index;
    int currentTimeStep =0;
    int numOfStage = 0;
    final String pathLogGame = "/engine/data/logGame";
    String gameStage[];
    public LogFile () {
        currentTimeStep = 0;
    }
    
    public String[] getLogFile(String _fileName) throws FileNotFoundException, IOException {
        this.fileName = _fileName;
        gameStage = new String[24000];
        System.out.println((pathLogGame + "/" + fileName + ".txt").toString());
        Scanner scanner = new Scanner(getClass().getResourceAsStream(pathLogGame + "/" + fileName + ".txt"));
         String input ;

     
        
        int index =0 ;
        while (scanner.hasNextLine()) {
            input = scanner.nextLine();
            gameStage[index++] = input;
            
        }
        
        numOfStage = index;
        
        scanner.close();

        return gameStage;
    }
    
    public String getNextStage () {
        if (currentTimeStep < numOfStage) return gameStage[currentTimeStep++];
        else return null;
    }
    
     public String getCurrentState () {
        if (currentTimeStep < numOfStage) return gameStage[currentTimeStep];
        else return null;
    }
}

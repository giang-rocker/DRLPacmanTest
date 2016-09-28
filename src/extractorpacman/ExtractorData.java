/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package extractorpacman;

import engine.pacman.game.Constants;
import engine.pacman.game.Constants.GHOST;
import static engine.pacman.game.Constants.MOVE.*;

import engine.pacman.game.Game;
import java.io.IOException;
import java.util.Arrays;
import static java.util.Objects.isNull;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Giang
 */
public class ExtractorData {

    Game game;
    String fileName;
    LogFile logFile;
    // 26x29 : shape of maze
    int frameMiniMap[][];

    // noPill: 0; pill:1
    int framePill[][];
    int framePowerPill[][];

    // no Pacman: 0, Pacman: 1
    int framePacmanPosition[][];
    int framePacmanLeft[][];
    int framePacmanRight[][];
    int framePacmanUp[][];
    int framePacmanDown[][];
    int framePacmanHorizontal0[][];
    int framePacmanHorizontal1[][];
    int framePacmanHorizontal2[][];
    int framePacmanHorizontal3[][];
    int framePacmanVerhicel0[][];
    int framePacmanVerhicel1[][];
    int framePacmanVerhicel2[][];
    int framePacmanVerhicel3[][];

    // noGhost: 0 , nomal ghost: 1 || eldibleGhost: -1
    int frameGhostPosition[][];
    int frameGhostLeft[][];
    int frameGhostRight[][];
    int frameGhostUp[][];
    int frameGhostDown[][];
    int frameGhostHorizontal0[][];
    int frameGhostHorizontal1[][];
    int frameGhostHorizontal2[][];
    int frameGhostHorizontal3[][];
    int frameGhostVerhicel0[][];
    int frameGhostVerhicel1[][];
    int frameGhostVerhicel2[][];
    int frameGhostVerhicel3[][];

    int frameTime[][];
    int frameLevel[][];
    int frameLiveLeft[][];

    int defaultX = 30;
    int defaultY = 28;

    public void loadGameFromGameState(String gameState)   {
        
       this.game = new Game(0,0);
        this.game.setGameState(gameState); // first gameStage
         this.extractData();
    }

    public ExtractorData(){
    _init();
    }
    public void _init() {
        
        if(isNull(this.game))
        this.game = new Game(0,0);
        
        frameMiniMap = new int[defaultX][defaultY];
        framePill = new int[defaultX][defaultY];
        framePowerPill = new int[defaultX][defaultY];

        // no Pacman: 0, Pacman: 1
        framePacmanPosition = new int[defaultX][defaultY];
        framePacmanLeft = new int[defaultX][defaultY];
        framePacmanRight = new int[defaultX][defaultY];
        framePacmanUp = new int[defaultX][defaultY];
        framePacmanDown = new int[defaultX][defaultY];
        framePacmanHorizontal0 = new int[defaultX][defaultY];
        framePacmanHorizontal1 = new int[defaultX][defaultY];
        framePacmanHorizontal2 = new int[defaultX][defaultY];
        framePacmanHorizontal3 = new int[defaultX][defaultY];
        framePacmanVerhicel0 = new int[defaultX][defaultY];
        framePacmanVerhicel1 = new int[defaultX][defaultY];
        framePacmanVerhicel2 = new int[defaultX][defaultY];
        framePacmanVerhicel3 = new int[defaultX][defaultY];

        // noGhost: 0 , nomal ghost: 1 || eldibleGhost: -1
        frameGhostPosition = new int[defaultX][defaultY];
        frameGhostLeft = new int[defaultX][defaultY];
        frameGhostRight = new int[defaultX][defaultY];
        frameGhostUp = new int[defaultX][defaultY];
        frameGhostDown = new int[defaultX][defaultY];
        frameGhostHorizontal0 = new int[defaultX][defaultY];
        frameGhostHorizontal1 = new int[defaultX][defaultY];
        frameGhostHorizontal2 = new int[defaultX][defaultY];
        frameGhostHorizontal3 = new int[defaultX][defaultY];
        frameGhostVerhicel0 = new int[defaultX][defaultY];
        frameGhostVerhicel1 = new int[defaultX][defaultY];
        frameGhostVerhicel2 = new int[defaultX][defaultY];
        frameGhostVerhicel3 = new int[defaultX][defaultY];

        frameTime = new int[defaultX][defaultY];
        frameLevel = new int[defaultX][defaultY];
        frameLiveLeft = new int[defaultX][defaultY];

        // RESET DATA
        for (int i =0; i < defaultX; i++) {
        Arrays.fill(frameMiniMap[i], 0); // path only

        Arrays.fill(framePill[i], 0);
        Arrays.fill(framePowerPill[i], 0);

        // 12 frame
        Arrays.fill(framePacmanLeft[i], 0);
        Arrays.fill(framePacmanRight[i], 0);
        Arrays.fill(framePacmanUp[i], 0);
        Arrays.fill(framePacmanDown[i], 0);
        Arrays.fill(framePacmanHorizontal0[i], 0);
        Arrays.fill(framePacmanHorizontal1[i], 0);
        Arrays.fill(framePacmanHorizontal2[i], 0);
        Arrays.fill(framePacmanHorizontal3[i], 0);
        Arrays.fill(framePacmanVerhicel0[i], 0);
        Arrays.fill(framePacmanVerhicel1[i], 0);
        Arrays.fill(framePacmanVerhicel2[i], 0);
        Arrays.fill(framePacmanVerhicel3[i], 0);

        // 12 frame
        Arrays.fill(frameGhostLeft[i], 0);
        Arrays.fill(frameGhostRight[i], 0);
        Arrays.fill(frameGhostUp[i], 0);
        Arrays.fill(frameGhostDown[i], 0);
        Arrays.fill(frameGhostHorizontal0[i], 0);
        Arrays.fill(frameGhostHorizontal1[i], 0);
        Arrays.fill(frameGhostHorizontal2[i], 0);
        Arrays.fill(frameGhostHorizontal3[i], 0);
        Arrays.fill(frameGhostVerhicel0[i], 0);
        Arrays.fill(frameGhostVerhicel1[i], 0);
        Arrays.fill(frameGhostVerhicel2[i], 0);
        Arrays.fill(frameGhostVerhicel3[i], 0);

        Arrays.fill(frameTime[i], 0);
        Arrays.fill(frameLevel[i], 0);
        Arrays.fill(frameLiveLeft[i], 0);
        }
    }

    public void extractData() {
        _init();

        //SET UP MINIMAP PATH
        for (int i = 0; i < game.getNumberOfNodes(); i++) {
            int x = game.getNodeYCood(i) / 4;
            int y = game.getNodeXCood(i) / 4;

            frameMiniMap[x][y] = 1;
            
            if(game.getPillIndex(i)!=-1)
            if ( game.isPillStillAvailable(game.getPillIndex(i))) {
                framePill[x][y] = 1;
            }
            
            if(game.getPowerPillIndex(i)!=-1)
            if (game.isPowerPillStillAvailable(game.getPowerPillIndex(i))) {
                framePowerPill[x][y] = 1;
            }

        }

        // SETUP PACMAN POSITION    
        {
            int x = game.getNodeYCood(game.getPacmanCurrentNodeIndex()) / 4;
            int y = game.getNodeXCood(game.getPacmanCurrentNodeIndex()) / 4;
            
            System.out.println(x +"- " + y);
            framePacmanPosition[x][y] = 1;

            // SETUP PACMAN LEFT RIGHT UP DOWN
            switch (game.getPacmanLastMoveMade()) {
                case LEFT:
                    framePacmanLeft[x][y] = 1;
                    break;
                case RIGHT:
                    framePacmanRight[x][y] = 1;
                    break;
                case UP:
                    framePacmanUp[x][y] = 1;
                    break;
                case DOWN:
                    framePacmanDown[x][y] = 1;
                    break;

            }

            //SETUP PACMAN HORIZONTAL VERHICLE
            switch (x % 4) {
                case 0:
                    framePacmanHorizontal0[x][y] = 1;
                    break;
                case 1:
                    framePacmanHorizontal1[x][y] = 1;
                    break;
                case 2:
                    framePacmanHorizontal2[x][y] = 1;
                    break;
                case 3:
                    framePacmanHorizontal3[x][y] = 1;
                    break;
            }

            switch (y % 4) {
                case 0:
                    framePacmanVerhicel0[x][y] = 1;
                    break;
                case 1:
                    framePacmanVerhicel1[x][y] = 1;
                    break;
                case 2:
                    framePacmanVerhicel2[x][y] = 1;
                    break;
                case 3:
                    framePacmanVerhicel3[x][y] = 1;
                    break;
            }

        }

        // SETUP GHOST POSITION  
        for (GHOST ghost : GHOST.values()) {
            int x = game.getNodeYCood(game.getGhostCurrentNodeIndex(ghost)) / 4;
            int y = game.getNodeXCood(game.getGhostCurrentNodeIndex(ghost)) / 4;

            frameGhostPosition[x][y] = 1;

            // SETUP PACMAN LEFT RIGHT UP DOWN
            switch (game.getGhostLastMoveMade(ghost)) {
                case LEFT:
                    frameGhostLeft[x][y] = 1;
                    break;
                case RIGHT:
                    frameGhostRight[x][y] = 1;
                    break;
                case UP:
                    frameGhostUp[x][y] = 1;
                    break;
                case DOWN:
                    frameGhostDown[x][y] = 1;
                    break;

            }

            //SETUP PACMAN HORIZONTAL VERHICLE
            switch (x % 4) {
                case 0:
                    frameGhostHorizontal0[x][y] = 1;
                    break;
                case 1:
                    frameGhostHorizontal1[x][y] = 1;
                    break;
                case 2:
                    frameGhostHorizontal2[x][y] = 1;
                    break;
                case 3:
                    frameGhostHorizontal3[x][y] = 1;
                    break;
            }

            switch (y % 4) {
                case 0:
                    frameGhostVerhicel0[x][y] = 1;
                    break;
                case 1:
                    frameGhostVerhicel1[x][y] = 1;
                    break;
                case 2:
                    frameGhostVerhicel2[x][y] = 1;
                    break;
                case 3:
                    frameGhostVerhicel3[x][y] = 1;
                    break;
            }

        }
        
        for (int i =0; i < defaultX; i++){
        Arrays.fill(frameLevel[i], game.getCurrentLevel());
        Arrays.fill(frameTime[i], game.getTotalTime());
        Arrays.fill(frameLiveLeft[i], game.getPacmanNumberOfLivesRemaining());
        }

    }
 
}

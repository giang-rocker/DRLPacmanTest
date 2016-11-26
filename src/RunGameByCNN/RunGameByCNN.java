/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package RunGameByCNN;

import engine.pacman.controllers.HumanController;
import engine.pacman.game.Constants;
import engine.pacman.game.Constants.MOVE;
import engine.pacman.game.Game;
import engine.pacman.game.GameView;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.EnumMap;
import java.util.Random;

/**
 *
 * @author giang-rocker
 */
public class RunGameByCNN {

    public static MOVE getMove(int ret) {
        MOVE nextMove = MOVE.NEUTRAL;
        switch (ret) {
            case 1:
                nextMove = MOVE.DOWN;
                break;
            case 2:
                nextMove = MOVE.LEFT;
                break;
            case 3:
                nextMove = MOVE.UP;
                break;
            case 4:
                nextMove = MOVE.RIGHT;
                break;
            default:
                nextMove = MOVE.NEUTRAL;
                break;
        }
        return nextMove;
    }

    public static String getMoveString(MOVE ret) {
        String stringMove = "";
        switch (ret) {
            case DOWN:
                stringMove = "DOWN";
                break;
            case LEFT:
                stringMove = "LEFT";
                break;
            case UP:
                stringMove = "UP";
                break;
            case RIGHT:
                stringMove = "RIGHT";
                break;
            default:
                stringMove = "NEUTRAL";
                break;
        }
        return stringMove;
    }

    public static void main(String[] args) throws IOException {
        int numOfGame = 0;
        int maxScore = 0;
        int maxLevel=0;
        int maxTime = 0;
        int bestRecord = 0;
        int perRandom = 0;
        ServerSocket s = new ServerSocket(22009);//22009
        System.out.println("HOSTNAME: " + InetAddress.getLocalHost().getHostName());

        Socket ss;
       // FormRunCNN formRunCNN = new FormRunCNN();
       // formRunCNN.setVisible(true);
        Game game = new Game(0);
        MOVE nextMove = MOVE.NEUTRAL;
       // String stringMove = "";
        boolean visual = true;
        
        float percentTranning = 0;

        PrintWriter pw;
        BufferedReader inFromPython;
        BufferedReader outToPython;
        try {
            ss = s.accept();
            pw = new PrintWriter(ss.getOutputStream(), true);

            System.out.println("Client python connected.. Waiting for Command");

        } finally {
        }

        while (true) {
          
            outToPython = new BufferedReader(new InputStreamReader(System.in));
            inFromPython = new BufferedReader(new InputStreamReader(ss.getInputStream()));
            int timeStep = 0;
            String command = inFromPython.readLine();

           // if (command.indexOf("TRANNING") != -1) {
            //    percentTranning = Float.parseFloat(command.substring(("TRANNING").length()));
              //  formRunCNN.setValue(stringMove, game.getTotalTime(), game.getScore(), numOfGame, bestRecord, maxScore, maxTime,maxLevel, true, percentTranning);
            //    continue;
           // } else 
           if (command.equals("START_GAME")) {
                if (game.getScore() > maxScore) {
                    maxScore = game.getScore();
                    maxTime = game.getTotalTime();
                    bestRecord = numOfGame;
                    maxLevel = game.getCurrentLevel();
                }

                BufferedWriter bw = null;
                
                if(numOfGame>0)
                try {
                    bw = new BufferedWriter(new FileWriter("LogRecord.txt", true));
                    String random ="";
                    if(perRandom == game.getTotalTime())
                        random = "RANDOM";
                    bw.write(numOfGame + "," + String.valueOf(game.getScore())+","+String.valueOf(game.getTotalTime())+","+String.valueOf(game.levelCount) +","+random);
                    bw.newLine();
                    bw.flush();
                } catch (IOException ioe) {
                    ioe.printStackTrace();
                } finally { // always close the file
                    if (bw != null) {
                        try {
                            bw.close();
                        } catch (IOException ioe2) {
                            // just ignore it
                        }
                    }
                }

                numOfGame++;
                game = new Game(0);
                pw.println(game.getGameState());
                perRandom = 0;

            }  
           else if (game.gameOver()) {
                    pw.println("GAME "+ numOfGame +" OVER - Score :" + game.getScore() + " T: " + game.getTotalTime() +" L: "+ game.getCurrentLevel() + " R: "  +((int) (perRandom*100/game.getTotalTime())));
                    
                } 
            
            else {
               // System.out.println("GIVE MOVE");
                String moveString="";
                // if RANDOM
                if (command.equals("RANDOM")) {
                    perRandom++;
                  Random R = new Random();
                  
                  MOVE[] listPosMove = game.getPossibleMoves(game.getPacmanCurrentNodeIndex(), game.getPacmanLastMoveMade());
                  nextMove = listPosMove[R.nextInt(listPosMove.length)];  
            //      moveString = nextMove.toString();
                  
                }
                // NO NEED to train
                else if ( game.getNodeXCood(game.getPacmanCurrentNodeIndex())%4!=0 || game.getNodeYCood(game.getPacmanCurrentNodeIndex())%4!=0 ){
                   nextMove = game.getPacmanLastMoveMade();
                }
                else{                
              //  moveString = command;
                // convert to int
                int ret = Integer.parseInt(command);
                nextMove = getMove(ret);
                }
                
                // check valid move
                // not allow wrong move
                
                boolean forceToGameOver = false;
                // force to die when can not finnnish a game or give a wrong move
                if (game.getNeighbour(game.getPacmanCurrentNodeIndex(), nextMove) ==-1)
                {
                   forceToGameOver = true;
                }
                else
                {
                    // simulate ghost move
                    Game simulatedGame = game.copy(false);
                    SimulateGhostMove ghostsMove = new SimulateGhostMove();
                    EnumMap<Constants.GHOST, MOVE> listGhostMove = new EnumMap<>(Constants.GHOST.class);
                    listGhostMove = ghostsMove.getMove(simulatedGame);
                   
                    game.advanceGame(nextMove,listGhostMove);
                      
                    
                }
            // write game state to python
            // w rite gamestate backc in anycase
           if(forceToGameOver){
                game.totalTime++;
                game.pacman.lastMoveMade = nextMove;
                game.gameOver = true;
                game.pacmanWasEaten = true;
            }
            
            pw.println(game.getGameState());
            }
 
         //   formRunCNN.setValue(stringMove, game.getTotalTime(), game.getScore(), numOfGame, bestRecord, maxScore, maxTime, maxLevel, game.gameOver(), percentTranning);
        }

    }

}

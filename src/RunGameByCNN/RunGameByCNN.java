/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package RunGameByCNN;

import engine.pacman.game.Constants;
import engine.pacman.game.Constants.MOVE;
import engine.pacman.game.Game;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.EnumMap;

/**
 *
 * @author giang-rocker
 */
public class RunGameByCNN {

    public static void main(String[] args) throws IOException {

        ServerSocket s = new ServerSocket(5000);

        FormRunCNN formRunCNN = new FormRunCNN();
        formRunCNN.setVisible(true);
        Game game = new Game(0);
        MOVE nextMove = MOVE.NEUTRAL;
        String stringMove = "";

        PrintWriter pw;
        BufferedReader inFromPython;
        BufferedReader outToPython;
        try {
            Socket ss = s.accept();
            pw = new PrintWriter(ss.getOutputStream(), true);
            outToPython = new BufferedReader(new InputStreamReader(System.in));
            inFromPython = new BufferedReader(new InputStreamReader(ss.getInputStream()));

            System.out.println("Client python connected.. Waiting for Command");

        } finally {
        }

        while (true) {
            String oldGameState = "";
            String command = inFromPython.readLine();
            if (command.equals("START_GAME")) {
                game = new Game(0);
                oldGameState = game.getGameState();
            } else {
                oldGameState = game.getGameState();
                // if not start game, it should be a move for current Game
                String moveString = command;
                // convert to int
                int ret = Integer.parseInt(command);

                // simulate ghost move
                Game simulatedGame = game.copy(false);
                SimulateGhostMove ghostsMove = new SimulateGhostMove();
                EnumMap<Constants.GHOST, MOVE> listGhostMove = new EnumMap<>(Constants.GHOST.class);
                listGhostMove = ghostsMove.getMove(simulatedGame);

                // convert to MOVE
                switch (ret) {
                    case 0:
                        nextMove = MOVE.DOWN;
                        stringMove = "DOWN";
                        break;
                    case 1:
                        nextMove = MOVE.LEFT;
                        stringMove = "LEFT";
                        break;
                    case 2:
                        nextMove = MOVE.UP;
                        stringMove = "UP";
                        break;
                    case 3:
                        nextMove = MOVE.RIGHT;
                        stringMove = "RIGHT";
                        break;
                    case 4:
                        nextMove = MOVE.NEUTRAL;
                        stringMove = "NEUTRAL";
                        break;
                }

                // advance
                game.advanceGame(nextMove, listGhostMove);

            }
            // write game state to python
            if (!game.gameOver()) {
                //   outToPython.read(target)
                pw.println(game.getGameState());
            } else {
                pw.println("GAME_OVER");
            }

            formRunCNN.setValue(stringMove, oldGameState, game.getGameState());
        }

    }

}

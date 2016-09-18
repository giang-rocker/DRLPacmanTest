/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package extractorpacman;

import engine.pacman.game.Constants.GHOST;
import java.awt.Color;
import java.awt.Graphics;
import engine.pacman.game.Game;
import engine.pacman.game.internal.Node;
import java.awt.Button;
import java.awt.Checkbox;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.Rectangle;
import java.awt.Shape;
import java.awt.event.ActionEvent;
import java.awt.image.ImageObserver;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.io.IOException;
import static java.lang.Thread.sleep;
import java.text.AttributedCharacterIterator;
import static java.util.Objects.isNull;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JPanel;
import javax.swing.plaf.basic.BasicComboBoxUI;

/**
 *
 * @author giang-rocker
 */
public class ExtractorForm extends javax.swing.JFrame {

    /**
     * Creates new form ExtractorForm
     */
    Game game;
    int scale = 6;
    int margin = 50;
    int defaultWidth = 108;
    int defaultHeight = 116;
    int maze[][];
    int minimizeW, minimizeH;
    int minX = 500, minY = 500;
    String fileName ;
    int maxX = 0, maxY = 0;

    int[][] minimizeMazeH;
    int[][] minimizeMazeW;
    int[][] minimizeMaze;

    Checkbox btnCheckDrawEmptyCell;
    Checkbox btnCheckDrawPill;
    Checkbox btnCheckDrawPath;
    Checkbox btnCheckDrawGhost;
    Checkbox btnCheckDrawPacman;
    Button btnNextStage;
    
    
    int timeStep;
    
    public void initControl() {

        int PosY = 10;

        btnCheckDrawEmptyCell = new Checkbox();
        btnCheckDrawEmptyCell.setForeground(Color.white);
        btnCheckDrawEmptyCell.setLabel("DrawEmptyCell");
        btnCheckDrawEmptyCell.setLocation(10, PosY);
        btnCheckDrawEmptyCell.setSize(130, 30);
        btnCheckDrawEmptyCell.setBackground(Color.black);
        btnCheckDrawEmptyCell.setVisible(true);
        btnCheckDrawEmptyCell.setState(true);

        btnCheckDrawPill = new Checkbox();
        btnCheckDrawPill.setForeground(Color.white);
        btnCheckDrawPill.setLabel("DrawPill");
        btnCheckDrawPill.setLocation(140, PosY);
        btnCheckDrawPill.setSize(90, 30);
        btnCheckDrawPill.setBackground(Color.black);
        btnCheckDrawPill.setVisible(true);
        btnCheckDrawPill.setState(true);

        btnCheckDrawPath = new Checkbox();
        btnCheckDrawPath.setForeground(Color.white);
        btnCheckDrawPath.setLabel("DrawPath");
        btnCheckDrawPath.setLocation(230, PosY);
        btnCheckDrawPath.setSize(90, 30);
        btnCheckDrawPath.setBackground(Color.black);
        btnCheckDrawPath.setVisible(true);
        btnCheckDrawPath.setState(true);

        btnCheckDrawPacman = new Checkbox();
        btnCheckDrawPacman.setForeground(Color.white);
        btnCheckDrawPacman.setLabel("DrawPacMan");
        btnCheckDrawPacman.setLocation(320, PosY);
        btnCheckDrawPacman.setSize(120, 30);
        btnCheckDrawPacman.setBackground(Color.black);
        btnCheckDrawPacman.setVisible(true);
        btnCheckDrawPacman.setState(true);

        btnCheckDrawGhost = new Checkbox();
        btnCheckDrawGhost.setForeground(Color.white);
        btnCheckDrawGhost.setLabel("DrawGhosts");
        btnCheckDrawGhost.setLocation(450, PosY);
        btnCheckDrawGhost.setSize(120, 30);
        btnCheckDrawGhost.setBackground(Color.black);
        btnCheckDrawGhost.setVisible(true);
        btnCheckDrawGhost.setState(true);
        
        btnNextStage = new Button();
        btnNextStage.setForeground(Color.white);
        btnNextStage.setLabel("Next Stage");
        btnNextStage.setLocation(670, PosY);
        btnNextStage.setSize(120, 30);
        btnNextStage.setBackground(Color.black);
        btnNextStage.setVisible(true);
       
        btnCheckDrawEmptyCell.addItemListener(new java.awt.event.ItemListener() {
            public void itemStateChanged(java.awt.event.ItemEvent evt) {
                chageState(evt);
            }
        });
        btnCheckDrawPill.addItemListener(new java.awt.event.ItemListener() {
            public void itemStateChanged(java.awt.event.ItemEvent evt) {
                chageState(evt);
            }
        });
        btnCheckDrawPacman.addItemListener(new java.awt.event.ItemListener() {
            public void itemStateChanged(java.awt.event.ItemEvent evt) {
                chageState(evt);
            }
        });
        btnCheckDrawGhost.addItemListener(new java.awt.event.ItemListener() {
            public void itemStateChanged(java.awt.event.ItemEvent evt) {
                chageState(evt);
            }
        });
        btnCheckDrawPath.addItemListener(new java.awt.event.ItemListener() {
            public void itemStateChanged(java.awt.event.ItemEvent evt) {
                chageState(evt);
            }
        });
        
        btnNextStage.addActionListener(new java.awt.event.ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
               clickNextStage(e);
                
            }
        });

        this.add(btnCheckDrawEmptyCell);
        this.add(btnCheckDrawPill);
        this.add(btnCheckDrawPath);
        this.add(btnCheckDrawPacman);
        this.add(btnCheckDrawGhost);
        this.add(btnNextStage);
    }
 

    public ExtractorForm(Game _game) {
        if(isNull(_game)) _game = new Game(0,3);
        initComponents();
        initControl();
        maze = new int[defaultHeight + 1][defaultWidth + 1];

        this.game = _game;
        for (Node node : game.getCurrentMaze().graph) {

            int nodeIndex = node.nodeIndex;

            int x = game.getNodeYCood(nodeIndex);
            int y = game.getNodeXCood(nodeIndex);

            if (game.getPillIndex(nodeIndex) != -1) {
                maze[x][y] = game.getPillIndex(nodeIndex)+1;
            } else {
                maze[x][y] = -1;
            }

            if (x < minX) {
                minX = x;
            }
            if (y < minY) {
                minY = y;
            }
            if (x > maxX) {
                maxX = x;
            }
            if (y > maxY) {
                maxY = y;
            }
        }

        this.setSize(margin * 2 + defaultWidth * scale + 300, margin * 2 + defaultHeight * scale);
        System.out.println((margin * 2 + defaultWidth * scale) + " " + (margin * 2 + defaultHeight * scale));

        minimizeMazeH = new int[defaultHeight + 1][defaultWidth + 1];
        minimizeMazeW = new int[defaultHeight + 1][defaultWidth + 1];
        minimizeMaze = new int[defaultHeight + 1][defaultWidth + 1];

        int index = 0;
        for (int i = minX; i <= maxX; i++) {
            boolean f = false;
            for (int j = minY; j <= maxY; j++) {
                if (maze[i][j] >0) {

                    for (int k = minY; k <= maxY; k++) {
                        minimizeMazeW[index][k] = maze[i][k];
                    }

                    index++;
                    f = true;
                }
                if (f) {
                    break;
                }
            }
        }
        minimizeH = index;

        index = 0;
        for (int j = minY; j <= maxY; j++) {
            boolean f = false;
            for (int i = 0; i < minimizeH; i++) {
                if (minimizeMazeW[i][j] >0) {

                    for (int k = 0; k < minimizeH; k++) {
                        minimizeMaze[k][index] = minimizeMazeW[k][j];
                    }

                    index++;
                    break;
                }
                if (f) {
                    break;
                }
            }
        }

        minimizeW = index;
        System.out.println(minimizeW + " " + minimizeH);
        paint(this.getGraphics());
    }
    
    LogFile logFile ;
    
    public void init (String _fileName ) throws IOException {
        this.fileName = _fileName;
        
        logFile = new LogFile();
        logFile.getLogFile(_fileName);
        
        
        this.game.setGameState(logFile.getNextStage());
         maze = new int[defaultHeight + 1][defaultWidth + 1];

       
        for (Node node : game.getCurrentMaze().graph) {

            int nodeIndex = node.nodeIndex;

            int x = game.getNodeYCood(nodeIndex);
            int y = game.getNodeXCood(nodeIndex);

            if (game.getPillIndex(nodeIndex) != -1) {
                maze[x][y] = game.getPillIndex(nodeIndex)+1;
            } else {
                maze[x][y] = -1;
            }

            if (x < minX) {
                minX = x;
            }
            if (y < minY) {
                minY = y;
            }
            if (x > maxX) {
                maxX = x;
            }
            if (y > maxY) {
                maxY = y;
            }
        }

        this.setSize(margin * 2 + defaultWidth * scale + 300, margin * 2 + defaultHeight * scale);
        System.out.println((margin * 2 + defaultWidth * scale) + " " + (margin * 2 + defaultHeight * scale));

        minimizeMazeH = new int[defaultHeight + 1][defaultWidth + 1];
        minimizeMazeW = new int[defaultHeight + 1][defaultWidth + 1];
        minimizeMaze = new int[defaultHeight + 1][defaultWidth + 1];

        int index = 0;
        for (int i = minX; i <= maxX; i++) {
            boolean f = false;
            for (int j = minY; j <= maxY; j++) {
                if (maze[i][j] >0) {

                    for (int k = minY; k <= maxY; k++) {
                        minimizeMazeW[index][k] = maze[i][k];
                    }

                    index++;
                    f = true;
                }
                if (f) {
                    break;
                }
            }
        }
        minimizeH = index;

        index = 0;
        for (int j = minY; j <= maxY; j++) {
            boolean f = false;
            for (int i = 0; i < minimizeH; i++) {
                if (minimizeMazeW[i][j] >0) {

                    for (int k = 0; k < minimizeH; k++) {
                        minimizeMaze[k][index] = minimizeMazeW[k][j];
                    }

                    index++;
                    break;
                }
                if (f) {
                    break;
                }
            }
        }

        minimizeW = index;
        System.out.println(minimizeW + " " + minimizeH);
        paint(this.getGraphics());
        
        
    
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jCheckBox1 = new javax.swing.JCheckBox();

        jCheckBox1.setText("jCheckBox1");

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setTitle("ExtractorForm");
        setBackground(new java.awt.Color(0, 0, 0));
        setForeground(java.awt.Color.black);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 748, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 796, Short.MAX_VALUE)
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents
    private void chageState(java.awt.event.ItemEvent evt) {
        // TODO add your handling code here:
        this.repaint();
    } 
    private void clickNextStage(java.awt.event.ActionEvent evt) {
        // TODO add your handling code here:
       String gameStage = logFile.getNextStage();
        
        if (!isNull(gameStage)){
        game.setGameState(gameStage);
        this.repaint();
        }
    }
   
    
    public void autoNextStage() {
       
        String gameStage = logFile.getNextStage();
        
        while (!isNull(gameStage) && gameStage !=""){
        game.setGameState(gameStage);
         
        try {
            sleep(20);
        } catch (InterruptedException ex) {
            Logger.getLogger(ExtractorForm.class.getName()).log(Level.SEVERE, null, ex);
        }
        
         gameStage = logFile.getNextStage();
         
         this.paint(this.getGraphics());
         
        }
        
        
    }
    
    public void drawPacman () {
       
         
        
    
    }
    
    public void paint(Graphics g) {
       
               
        g.setColor(Color.black);
        g.fillRect(0, 0, margin * 2 + defaultWidth * scale + 400, margin * 2 + defaultHeight * scale);
        g.setColor(Color.white);

        g.drawRect(0, 0, margin * 2 + defaultWidth * scale - 1, margin * 2 + defaultHeight * scale - 1);

        for (int i = minX; i <= maxX; i++) {
            for (int j = minY; j <= maxY; j++) {

                if (btnCheckDrawEmptyCell.getState()) {
                    g.setColor(Color.DARK_GRAY);
                    g.fillRect(margin + j * scale + scale / 6, margin + i * scale + scale / 6, 2 * scale / 3, 2 * scale / 3);

                }

                if (maze[i][j] == 0) {
                    continue;
                }

                if (btnCheckDrawPath.getState()) {
                    g.setColor(Color.blue);
                    g.fillRect(margin + j * scale + scale / 6, margin + i * scale + scale / 6, 2 * scale / 3, 2 * scale / 3);

                }
                if (maze[i][j] >0 && btnCheckDrawPill.getState() && this.game.isPillStillAvailable(maze[i][j]-1)) {
                    g.setColor(Color.red);
                    g.fillRect(margin + j * scale + scale / 6, margin + i * scale + scale / 6, 2 * scale / 3, 2 * scale / 3);

                }

            
            }
        }

        // draw Pacman
        g.setColor(Color.YELLOW);
        int X = game.getNodeXCood(game.getPacmanCurrentNodeIndex());
        int Y = game.getNodeYCood(game.getPacmanCurrentNodeIndex());

        if (btnCheckDrawPacman.getState()) {
            g.fillOval(margin + X * scale - 4 * scale / 2, margin + Y * scale - 4 * scale / 2, 4 * scale, 4 * scale);
        }
        drawPacman () ;

        Color[] listGhostColor = new Color[]{Color.PINK, Color.CYAN, Color.GREEN, Color.RED};
        int index = 0;
        if (btnCheckDrawGhost.getState()) {
            for (GHOST ghost : GHOST.values()) {
                X = game.getNodeXCood(game.getGhostCurrentNodeIndex(ghost));
                 Y = game.getNodeYCood(game.getGhostCurrentNodeIndex(ghost));

                g.setColor(listGhostColor[index++]);
                
                if (game.isGhostEdible(ghost))
                    g.setColor(Color.blue);
                
                g.fillOval(margin + X * scale - 4 * scale / 2, margin + Y * scale - 4 * scale / 2, 4 * scale, 4 * scale);

            }
        }

        int marginMX = 800;
        int marginMY = 50;

        for (int i = 0; i < minimizeH; i++) {
            for (int j = 0; j < minimizeW; j++) {

                if (btnCheckDrawEmptyCell.getState()) {
                    g.setColor(Color.DARK_GRAY);
                    g.fillRect(marginMX + j * scale + scale / 6, marginMY + i * scale + scale / 6, 2 * scale / 3, 2 * scale / 3);

                }

                if (minimizeMaze[i][j] == 0) {
                    continue;
                }

                if (btnCheckDrawPath.getState()) {
                    g.setColor(Color.blue);
                    g.fillRect(marginMX + j * scale + scale / 6, marginMY + i * scale + scale / 6, 2 * scale / 3, 2 * scale / 3);

                }

                if (minimizeMaze[i][j] > 0 && btnCheckDrawPill.getState()&& this.game.isPillStillAvailable(minimizeMaze[i][j]-1)) {
                    g.setColor(Color.red);
                    g.fillRect(marginMX + j * scale + scale / 6, marginMY + i * scale + scale / 6, 2 * scale / 3, 2 * scale / 3);

                }

            }
        }

    }

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(ExtractorForm.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(ExtractorForm.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(ExtractorForm.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(ExtractorForm.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {

                ExtractorForm ex = new ExtractorForm(null);
                
                try {
                    ex.init("F000000");
                } catch (IOException ex1) {
                    Logger.getLogger(ExtractorForm.class.getName()).log(Level.SEVERE, null, ex1);
                }
                ex.setVisible(true);
                ex.autoNextStage();
                
            }
        });
    }


    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JCheckBox jCheckBox1;
    // End of variables declaration//GEN-END:variables
}

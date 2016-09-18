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
import java.awt.Checkbox;
import java.awt.Graphics2D;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
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

    int maxX = 0, maxY = 0;

    int[][] minimizeMazeH;
    int[][] minimizeMazeW;
    int[][] minimizeMaze;

    Checkbox btnCheckDrawEmptyCell;
    Checkbox btnCheckDrawPill;
    Checkbox btnCheckDrawPath;
    Checkbox btnCheckDrawGhost;
    Checkbox btnCheckDrawPacman;

    public void initCheckBox() {

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

        this.add(btnCheckDrawEmptyCell);
        this.add(btnCheckDrawPill);
        this.add(btnCheckDrawPath);
        this.add(btnCheckDrawPacman);
        this.add(btnCheckDrawGhost);
    }

    public class propertyChangeListener implements PropertyChangeListener {

        ExtractorForm ex;

        public propertyChangeListener(ExtractorForm _ex) {
            this.ex = _ex;
        }

        @Override
        public void propertyChange(PropertyChangeEvent evt) {
            System.out.println("HERE");
            ex.paint(ex.getGraphics());
        }

    }

    public ExtractorForm(Game _game) {
        initComponents();
        initCheckBox();
        maze = new int[defaultHeight + 1][defaultWidth + 1];

        this.game = _game;
        for (Node node : game.getCurrentMaze().graph) {

            int nodeIndex = node.nodeIndex;

            int x = game.getNodeYCood(nodeIndex);
            int y = game.getNodeXCood(nodeIndex);

            if (game.getPillIndex(nodeIndex) != -1) {
                maze[x][y] = 2;
            } else {
                maze[x][y] = 1;
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
        for(int i =minX; i<=maxX; i++){
            boolean f = false;
        for (int j = minY; j <= maxY; j++) {
            if (maze[i][j] == 2) {

                for (int k = minY; k <= maxY; k++) {
                    minimizeMazeW[index][k] = maze[i][k];
                }

                index++;
                f= true;
            }
            if (f) break;
        }
        }
         minimizeH = index;
       
        index = 0;
        for (int j=minY; j <= maxY; j++){
            boolean f = false;
        for (int i = 0; i < minimizeH; i++) {
            if (minimizeMazeW[i][j] == 2) {

                for (int k = 0; k < minimizeH; k++) {
                    minimizeMaze[k][index] = minimizeMazeW[k][j];
                }

                index++;
                break;
            }
             if (f) break;
        }
        }

        minimizeW = index;
        System.out.println(minimizeW + " " + minimizeH );
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

    public void paint(Graphics g) {
        g.setColor(Color.white);

        g.drawRect(0, 0, margin * 2 + defaultWidth * scale - 1, margin * 2 + defaultHeight * scale - 1);
        g.setColor(Color.black);

        g.fillRect(1, 1, margin * 2 + defaultWidth * scale + 400, margin * 2 + defaultHeight * scale);

        for (int i = minX; i <= maxX; i++) {
            for (int j = minY; j <= maxY; j++) {

                if (btnCheckDrawEmptyCell.getState()) {
                    g.setColor(Color.DARK_GRAY);
                    g.fillRect(margin + j * scale + scale / 6, margin + i * scale + scale / 6, 2 * scale / 3, 2 * scale / 3);

                }

                if (maze[i][j] == 1 && btnCheckDrawPath.getState()) {
                    g.setColor(Color.blue);
                } else if (maze[i][j] == 2 && btnCheckDrawPill.getState()) {
                    g.setColor(Color.red);
                } else {
                    continue;
                }

                g.fillRect(margin + j * scale + scale / 6, margin + i * scale + scale / 6, 2 * scale / 3, 2 * scale / 3);

            }
        }

        // draw Pacman
        g.setColor(Color.YELLOW);
        int X = game.getNodeXCood(game.getPacmanCurrentNodeIndex());
        int Y = game.getNodeYCood(game.getPacmanCurrentNodeIndex());

        if (btnCheckDrawPacman.getState()) {
            g.fillOval(margin + X * scale - 4 * scale / 2, margin + Y * scale - 4 * scale / 2, 4 * scale, 4 * scale);
        }

        Color[] listGhostColor = new Color[]{Color.PINK, Color.CYAN, Color.ORANGE, Color.RED};
        int index = 0;
        if (btnCheckDrawGhost.getState()) {
            for (GHOST ghost : GHOST.values()) {
                X = game.getNodeXCood(game.getGhostCurrentNodeIndex(ghost));
                Y = game.getNodeYCood(game.getGhostCurrentNodeIndex(ghost));

                g.setColor(listGhostColor[index++]);
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

                if (minimizeMaze[i][j] == 1 && btnCheckDrawPath.getState()) {
                    g.setColor(Color.blue);
                } else if (minimizeMaze[i][j] == 2 && btnCheckDrawPill.getState()) {
                    g.setColor(Color.red);
                } else {
                    continue;
                }

                g.fillRect(marginMX + j * scale + scale / 6, marginMY + i * scale + scale / 6, 2 * scale / 3, 2 * scale / 3);

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
                for (int i=0; i <4; i++ ){
                Game game = new Game(0,i);
                new ExtractorForm(game).setVisible(true);
                }
            }
        });
    }


    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JCheckBox jCheckBox1;
    // End of variables declaration//GEN-END:variables
}

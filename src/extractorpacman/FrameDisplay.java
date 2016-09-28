/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package extractorpacman;

import java.awt.Button;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Label;
import java.awt.event.ActionEvent;
import java.io.IOException;
import java.util.Arrays;
import static java.util.Objects.isNull;

/**
 *
 * @author Giang
 */
public class FrameDisplay extends javax.swing.JFrame {

    /**
     * Creates new form FrameDisplay
     */
    ExtractorData extractorData;
    int collectedArray[][][];

    int numOfArray = 32;
    int defaultX = 30;
    int defaultY = 28;
    int marginMX = 100;
    int marginMY = 100;
    int scale = 10;

    // controll
    Button btnNextFrame;
    Label lbFrameName;

    //list Frame Name
    String frameName[];

    public void setupControl() {
        //CONFIG CONTROLL
        btnNextFrame = new Button();
        btnNextFrame.setForeground(Color.white);
        btnNextFrame.setLabel("Next Frame");
        btnNextFrame.setLocation(30, 30);
        btnNextFrame.setSize(120, 30);
        btnNextFrame.setBackground(Color.black);
        btnNextFrame.setVisible(true);
        
        lbFrameName = new Label();
        lbFrameName.setForeground(Color.white);
        lbFrameName.setLocation(160, 30);
        lbFrameName.setSize(160, 30);
        lbFrameName.setVisible(true);
        lbFrameName.setBackground(Color.black);
        

        //ADD EVENT COTROL
        btnNextFrame.addActionListener(new java.awt.event.ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                clickNextFrame(e);

            }
        });

        //ADD CONTROL
        this.add(btnNextFrame);
        this.add(lbFrameName);
                

        // create frame name
        frameName = new String[]{
            "frameMiniMap", "framePill", "framePowerPill", "framePacmanPosition", "framePacmanLeft", "framePacmanRight", "framePacmanUp", "framePacmanDown", "framePacmanHorizontal0", "framePacmanHorizontal1", "framePacmanHorizontal2", "framePacmanHorizontal3", "framePacmanVerhicel0", "framePacmanVerhicel1", "framePacmanVerhicel2", "framePacmanVerhicel3", "frameGhostPosition", "frameGhostLeft", "frameGhostRight", "frameGhostUp", "frameGhostDown", "frameGhostHorizontal0", "frameGhostHorizontal1", "frameGhostHorizontal2", "frameGhostHorizontal3", "frameGhostVerhicel0", "frameGhostVerhicel1", "frameGhostVerhicel2", "frameGhostVerhicel3", "frameTime", "frameLevel", "frameLiveLeft"
        };
    }

    private void clickNextFrame(java.awt.event.ActionEvent evt) {
        currentFrame++;
        currentFrame %= numOfArray;
        this.repaint();
    }

    public FrameDisplay() {
        initComponents();
        setupControl();
        extractorData = new ExtractorData();
        collectedArray = new int[numOfArray][defaultX][defaultY];
        this.setSize(defaultX * scale + 2 * marginMX, defaultY * scale + 2 * marginMX);
    }

    public void collectArray() {
         collectedArray = new int[numOfArray][defaultX][defaultY];
         int index = 0;
        collectedArray[index++] = extractorData.frameMiniMap;
        collectedArray[index++] = extractorData.framePill;
        collectedArray[index++] = extractorData.framePowerPill;

        // no Pacman: 0, Pacman: 1
        collectedArray[index++] = extractorData.framePacmanPosition;
        collectedArray[index++] = extractorData.framePacmanLeft;
        collectedArray[index++] = extractorData.framePacmanRight;
        collectedArray[index++] = extractorData.framePacmanUp;
        collectedArray[index++] = extractorData.framePacmanDown;
        collectedArray[index++] = extractorData.framePacmanHorizontal0;
        collectedArray[index++] = extractorData.framePacmanHorizontal1;
        collectedArray[index++] = extractorData.framePacmanHorizontal2;
        collectedArray[index++] = extractorData.framePacmanHorizontal3;
        collectedArray[index++] = extractorData.framePacmanVerhicel0;
        collectedArray[index++] = extractorData.framePacmanVerhicel1;
        collectedArray[index++] = extractorData.framePacmanVerhicel2;
        collectedArray[index++] = extractorData.framePacmanVerhicel3;

        // noGhost: 0 , nomal ghost: 1 || eldibleGhost: -1
        collectedArray[index++] = extractorData.frameGhostPosition;
        collectedArray[index++] = extractorData.frameGhostLeft;
        collectedArray[index++] = extractorData.frameGhostRight;
        collectedArray[index++] = extractorData.frameGhostUp;
        collectedArray[index++] = extractorData.frameGhostDown;
        collectedArray[index++] = extractorData.frameGhostHorizontal0;
        collectedArray[index++] = extractorData.frameGhostHorizontal1;
        collectedArray[index++] = extractorData.frameGhostHorizontal2;
        collectedArray[index++] = extractorData.frameGhostHorizontal3;
        collectedArray[index++] = extractorData.frameGhostVerhicel0;
        collectedArray[index++] = extractorData.frameGhostVerhicel1;
        collectedArray[index++] = extractorData.frameGhostVerhicel2;
        collectedArray[index++] = extractorData.frameGhostVerhicel3;

        collectedArray[index++] = extractorData.frameTime;
        collectedArray[index++] = extractorData.frameLevel;
        collectedArray[index++] = extractorData.frameLiveLeft;

    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 200, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 200, Short.MAX_VALUE)
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    /**
     * @param args the command line arguments
     */
    int currentFrame = 0;

    public void paint(Graphics g) {

        g.setColor(Color.black);
        g.fillRect(0, 0, defaultX * scale + 2 * marginMX, defaultY * scale + 2 * marginMX);
        g.setColor(Color.white);
        g.drawRect(0, 0, defaultX * scale + 2 * marginMX - 1, defaultY * scale + 2 * marginMX - 1);
        
       lbFrameName.setText(frameName[currentFrame]);
        
        for (int i = 1; i < defaultX; i++) {
            for (int j = 0; j < defaultY; j++) {
                if (collectedArray[currentFrame][i][j] == 0) {
                    g.setColor(Color.DARK_GRAY);
                } else {
                    g.setColor(Color.green);
                }

                g.fillRect(marginMX + j * scale + scale / 6, marginMY + i * scale + scale / 6, 2 * scale / 3, 2 * scale / 3);
            }
        }

    }

    

    // Variables declaration - do not modify//GEN-BEGIN:variables
    // End of variables declaration//GEN-END:variables
}

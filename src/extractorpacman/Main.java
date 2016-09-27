/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package extractorPacman;

import java.util.Scanner;
public class Main {
    public static void main(String args[]) {
        Scanner in=new Scanner (System.in);
        
        while (in.hasNext()) {
            long a = in.nextLong();
            long b = in.nextLong();
            System.out.println(Math.abs(a-b));
        }
    }
    
}

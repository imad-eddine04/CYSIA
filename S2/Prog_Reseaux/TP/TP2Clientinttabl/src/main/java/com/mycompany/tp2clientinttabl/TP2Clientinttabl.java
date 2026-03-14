/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.mycompany.tp2clientinttabl;

import java.net.*;
import java.io.*;
import java.util.Scanner;
/**
 *
 * @author amine
 */
public class TP2Clientinttabl {

    public static void main(String[] args) {
        try {
            Socket sock = new Socket("localhost", 7777);
            DataOutputStream out = new DataOutputStream(sock.getOutputStream());
            DataInputStream in = new DataInputStream(sock.getInputStream());
            Scanner scanner = new Scanner(System.in);

            while (true) {
                System.out.print("Entrez un nombre : ");
                String numberStr = scanner.next();
                
                out.writeUTF(numberStr);
                out.flush();
                
                System.out.println("Table de multiplication");
                for (int i = 1; i <= 10; i++) {
                    String response = in.readUTF();
                    System.out.println(response);
                }

                if (numberStr.equals("0")) break;
            }

            sock.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
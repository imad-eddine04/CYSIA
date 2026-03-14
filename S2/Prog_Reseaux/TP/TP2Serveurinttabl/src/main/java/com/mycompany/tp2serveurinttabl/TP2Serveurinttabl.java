/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.mycompany.tp2serveurinttabl;

import java.net.*;
import java.io.*;
/**
 *
 * @author amine
 */
public class TP2Serveurinttabl {


    public static void main(String[] args) {
        try {
            ServerSocket server = new ServerSocket(7777);
            System.out.println("Serveur en attente");
            
            Socket sock = server.accept();
            DataInputStream in = new DataInputStream(sock.getInputStream());
            DataOutputStream out = new DataOutputStream(sock.getOutputStream());

            while (true) {
                try {
                    String input = in.readUTF();
                    int number = Integer.parseInt(input);
                    System.out.println("Client demande la table de : " + number);

                    for (int i = 1; i <= 10; i++) {
                        String line = number + " x " + i + " = " + (number * i);
                        out.writeUTF(line);
                    }
                    out.flush();

                    if (number == 0) break;
                } catch (EOFException e) {
                    break;
                }
            }

            sock.close();
            server.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
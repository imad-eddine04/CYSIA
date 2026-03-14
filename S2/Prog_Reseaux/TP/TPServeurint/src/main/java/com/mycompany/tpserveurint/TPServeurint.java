package com.mycompany.tpserveurint;

import java.net.*;
import java.io.*;

public class TPServeurint {

    public static void main(String[] args) {
        try {
            ServerSocket server = new ServerSocket(7777);
            System.out.println("Serveur en attente sur le port 7777...");
            
            Socket sock = server.accept();
            System.out.println("Client connecte.");

            DataInputStream in = new DataInputStream(sock.getInputStream());
            DataOutputStream out = new DataOutputStream(sock.getOutputStream());

            while (true) {
                try {
                    int number = in.readInt();
                    System.out.println("Nombre recu : " + number);
                    
                    int result = number * 10;
                    System.out.println("Calcul effectue : " + number + " * 10 = " + result);
                    
                    out.writeInt(result);
                    out.flush();
                    System.out.println("Resultat envoye.");

                    if (number == 0) break;
                } catch (EOFException e) {
                    break;
                }
            }

            sock.close();
            server.close();
            System.out.println("Serveur arrêté.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
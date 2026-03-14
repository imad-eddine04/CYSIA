package com.mycompany.tp3;
import java.net.*;
import java.io.*;

public class TP3 {
    public static void main(String[] args) {
        try {
            Socket sock = new Socket("localhost", 7777);
            System.out.println("Connected to server");

            PrintWriter out = new PrintWriter(sock.getOutputStream(), true);
            BufferedReader in = new BufferedReader(
                    new InputStreamReader(sock.getInputStream())
            );
            BufferedReader keyboard = new BufferedReader(
                    new InputStreamReader(System.in)
            );

            String msg;

            while (true) {
                msg = keyboard.readLine();
                out.println(msg);
                
                String response = in.readLine();
                System.out.println("Reponse du serveur: " + response);

                if (msg.equalsIgnoreCase("exit")) {
                    break;
                }
            }

            sock.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
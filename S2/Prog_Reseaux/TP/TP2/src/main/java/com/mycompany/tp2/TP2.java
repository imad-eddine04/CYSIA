package com.mycompany.tp2;
import java.net.*;
import java.io.*;

public class TP2 {
    public static void main(String[] args) {
        try {
            ServerSocket server = new ServerSocket(7777);
            System.out.println("Server started...");

            Socket sock = server.accept();
            System.out.println("Client connected");

            PrintWriter out = new PrintWriter(sock.getOutputStream(), true);
            BufferedReader in = new BufferedReader(
                    new InputStreamReader(sock.getInputStream())
            );

            String msg;

            while ((msg = in.readLine()) != null) {
                System.out.println("recu : " + msg);
                
                String upperMsg = msg.toUpperCase();
                out.println(upperMsg);

                if (msg.equalsIgnoreCase("exit")) {
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
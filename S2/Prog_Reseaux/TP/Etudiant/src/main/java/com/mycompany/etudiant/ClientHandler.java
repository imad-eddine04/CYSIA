/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.tp_multithread;

import java.io.*;
import java.net.*;
import java.util.Date;

public class ClientHandler implements Runnable {
    private Socket s;

    public ClientHandler(Socket s) {
        this.s = s;
    }

    @Override
    public void run() {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
            PrintWriter out = new PrintWriter(s.getOutputStream(), true);
            String message;
            String dernierMessage = "";
            int compteur = 0;

            while ((message = in.readLine()) != null) {
                if (message.equalsIgnoreCase("date")) {
                    out.println(new Date().toString());
                    dernierMessage = "";
                    compteur = 0;
                } else {
                    if (message.equals(dernierMessage)) {
                        compteur++;
                    } else {
                        dernierMessage = message;
                        compteur = 1;
                    }
                    if (compteur >= 3) {
                        System.out.println("Tentative de piratage !");
                        out.println("Connexion fermée : tentative de piratage.");
                        s.close();
                        return;
                    } else {
                        out.println("demande à reformuler");
                    }
                }
            }
        } catch (IOException e) {
            System.out.println("Client déconnecté.");
        }
    }
}
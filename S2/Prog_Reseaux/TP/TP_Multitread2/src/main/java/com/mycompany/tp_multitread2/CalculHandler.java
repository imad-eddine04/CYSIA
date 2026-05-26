/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.tp_multitread2;

import java.io.*;
import java.net.*;

public class CalculHandler implements Runnable {
    private final Socket socket;

    public CalculHandler(Socket socket) {
        this.socket = socket;
    }

    @Override
    public void run() {
        try (
            BufferedReader in = new BufferedReader(
                new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true)
        ) {
            String ligne;
            while ((ligne = in.readLine()) != null) {
                String[] parties = ligne.trim().split(" ");

                if (parties.length != 2) {
                    out.println("ERREUR : format attendu -> <message> <n>");
                    continue;
                }

                String operation = parties[0].toLowerCase();
                double n;

                try {
                    n = Double.parseDouble(parties[1]);
                } catch (NumberFormatException e) {
                    out.println("ERREUR : nombre invalide.");
                    continue;
                }

                String resultat = calculer(operation, n);
                System.out.println("[Port " + socket.getPort() + "] "
                    + operation + "(" + n + ") = " + resultat);
                out.println("Port " + socket.getPort()
                    + " | Résultat : " + resultat);
            }

        } catch (IOException e) {
            System.out.println("Client déconnecté.");
        }
    }

    private String calculer(String op, double n) {
        switch (op) {
            case "fac" -> {
                if (n < 0 || n != (int) n)
                    return "ERREUR : n doit être un entier >= 0 pour fac.";
                return "fac(" + (int)n + ") = " + factorielle((int) n);
            }

            case "rac" -> {
                if (n < 0)
                    return "ERREUR : n doit être >= 0 pour rac.";
                return "rac(" + n + ") = " + Math.sqrt(n);
            }

            case "car" -> {
                return "car(" + n + ") = " + (n * n);
            }

            default -> {
                return "ERREUR : opération inconnue. Utilisez fac, rac ou car.";
            }
        }
    }

    private long factorielle(int n) {
        if (n == 0 || n == 1) return 1;
        long result = 1;
        for (int i = 2; i <= n; i++) result *= i;
        return result;
    }
}
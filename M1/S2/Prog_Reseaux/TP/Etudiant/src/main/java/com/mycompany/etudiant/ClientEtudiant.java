package com.mycompany.etudiant;

import java.io.*;
import java.net.*;

public class ClientEtudiant {

    public static void main(String[] args) {

        try {
            Socket socket = new Socket("localhost", 5000);

            BufferedReader clavier = new BufferedReader(new InputStreamReader(System.in));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            ObjectInputStream in = new ObjectInputStream(socket.getInputStream());

            while (true) {
                System.out.println("Tapez un nom (q pour terminer): ");
                String nom = clavier.readLine();

                out.println(nom);

                if (nom.equalsIgnoreCase("q")) {
                    break;
                }

                Etudiant e = (Etudiant) in.readObject();

                if (e != null) {
                    System.out.println("Serveur -> Client : " + e);
                } else {
                    System.out.println("Etudiant non trouve");
                }
            }

            in.close();
            out.close();
            socket.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
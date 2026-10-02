package com.mycompany.etudiant;

import java.io.*;
import java.net.*;

public class ServerEtudiant {

    public static void main(String[] args) {

        try {
            ServerSocket serverSocket = new ServerSocket(5000);
            System.out.println("Serveur demarre...");
            System.out.println("En attente d'un client...");

            Socket socket = serverSocket.accept();
            System.out.println("Client connecte");

            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());

            Etudiant[] etudiants = {
                new Etudiant("Menad", "Amine", 21),
                new Etudiant("Saim Haddache", "SidAhmed", 21),
            };

            String nomRecu;
            while ((nomRecu = in.readLine()) != null) {
                
                if (nomRecu.equalsIgnoreCase("q")) {
                    System.out.println("Client a termine la session.");
                    break;
                }

                System.out.println("Recu : " + nomRecu);

                Etudiant etudiantTrouve = null;
                for (Etudiant e : etudiants) {
                    if (e.getNom().equalsIgnoreCase(nomRecu)) {
                        etudiantTrouve = e;
                        break;
                    }
                }

                out.writeObject(etudiantTrouve);
                out.flush(); 
                out.reset(); 
            }

            out.close();
            in.close();
            socket.close();
            serverSocket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
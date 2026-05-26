package com.mycompany.tp_multitread2;

/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author PC
 */
import java.io.*;
import java.net.*;

public class Serveur2 {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(6000);
        System.out.println("Serveur de calcul démarré sur le port 6000...");

        while (true) {
            Socket clientSocket = serverSocket.accept();
            System.out.println("Client connecté depuis port : "
                + clientSocket.getPort());
            new Thread(new CalculHandler(clientSocket)).start();
        }
    }
}
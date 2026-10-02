/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.etudiant;

/**
 *
 * @author PC
 */
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class Serveur {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(1234);
        while (true) {
            Socket s = serverSocket.accept();
            Thread t = new Thread(new ClientHandler(s));
            t.start();
        }
    }
}
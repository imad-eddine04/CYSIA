/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.tp_multithread;

/**
 *
 * @author PC
 */
import java.io.*;
import java.net.*;

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
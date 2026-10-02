/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.tp_multitread2;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Client2 {
    public static void main(String[] args) throws IOException {
        try (Socket socket = new Socket("localhost", 6000)) {
            System.out.println("Connecté au serveur (port local : "
                    + socket.getLocalPort() + ")");
            
            BufferedReader in = new BufferedReader(
                    new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            Scanner scanner = new Scanner(System.in);
            
            System.out.println("Format : <opération> <nombre>");
            System.out.println("Opérations : fac | rac | car");
            
            while (true) {
                System.out.print("> ");
                String msg = scanner.nextLine();
                if (msg.equalsIgnoreCase("exit")) break;
                out.println(msg);
                System.out.println("Serveur : " + in.readLine());
            }
        }
    }
}
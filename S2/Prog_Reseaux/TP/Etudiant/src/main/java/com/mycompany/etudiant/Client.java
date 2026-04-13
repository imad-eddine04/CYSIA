/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.etudiant;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Client {
    public static void main(String[] args) throws IOException {
        Socket s = new Socket("localhost", 1234);
        BufferedReader sin = new BufferedReader(new InputStreamReader(s.getInputStream()));
        PrintWriter sout = new PrintWriter(s.getOutputStream(), true);
        Scanner sc = new Scanner(System.in);

        while (true) {
            String msg = sc.nextLine();
            sout.println(msg);
            String reponse = sin.readLine();
            if (reponse == null) break;
            System.out.println("Serveur : " + reponse);
        }

        s.close();
    }
}
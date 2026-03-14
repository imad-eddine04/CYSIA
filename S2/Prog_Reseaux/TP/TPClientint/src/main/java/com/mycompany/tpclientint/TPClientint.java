/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.mycompany.tpclientint;
import java.net.*;
import java.io.*;
import java.util.Scanner;
/**
 *
 * @author amine
 */
public class TPClientint {

    public static void main(String[] args) {
        try {
            Socket sock = new Socket("localhost", 7777);

            DataOutputStream out = new DataOutputStream(sock.getOutputStream());
            DataInputStream in = new DataInputStream(sock.getInputStream());
            Scanner scanner = new Scanner(System.in);

            while (true) {
                int number = scanner.nextInt();
                
                out.writeInt(number);
                out.flush();
                
                int response = in.readInt();
                System.out.println(response);

                if (number == 0) break;
            }

            sock.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
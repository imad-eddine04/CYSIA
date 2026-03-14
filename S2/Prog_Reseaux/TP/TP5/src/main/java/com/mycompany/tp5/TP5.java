/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.mycompany.tp5;

/**
 *
 * @author Imad Hassi
 */
import java.io.*;
import java.net.*;

public class TP5 {
    public static void main(String argv[]) throws IOException {
        String msg = "JE SUIS ETUDIANT EN INFORMATIQUE";
        InetAddress group = InetAddress.getByName("230.0.0.0");
        MulticastSocket socket = new MulticastSocket(1000);
        socket.joinGroup(group);

        DatagramPacket hi = new DatagramPacket(msg.getBytes(),
            msg.length(), group, 1000);
        socket.send(hi);

        byte[] buf = new byte[1024];
        DatagramPacket recv = new DatagramPacket(buf, buf.length);
        socket.receive(recv);

        String ch = new String(recv.getData());
        System.out.println(ch);

        socket.leaveGroup(group);
    }
}

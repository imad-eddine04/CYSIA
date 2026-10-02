/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.mycompany.chatserver;
import java.io.*;
import java.net.*;
import java.util.*;
/**
 *
 * @author Imad Hassi
 */

public class ChatServer {
    // Shared thread-safe lists for active clients and registered usernames
    public static Vector<ChatService> activeClients = new Vector<>();
    public static Vector<String> registeredUsers = new Vector<>(); 

    public static void main(String[] args) {
        try {
            // Server starts on port 2000 as requested in your TD [4]
            ServerSocket serverSocket = new ServerSocket(2000);
            System.out.println("Server is running on port 2000...");

            while (true) {
                // Wait for a client connection request [5]
                Socket s = serverSocket.accept(); 
                ChatService service = new ChatService(s);
                activeClients.add(service);
                // Delegate to a dedicated thread for multi-client support [6, 7]
                new Thread(service).start(); 
            }
        } catch (IOException e) {
            System.err.println("Server Error: " + e.getMessage());
        }
    }

    // Broadcasts a message to all active users
    public static void broadcast(String message) {
        for (ChatService client : activeClients) {
            client.sendMessage(message);
        }
    }
}
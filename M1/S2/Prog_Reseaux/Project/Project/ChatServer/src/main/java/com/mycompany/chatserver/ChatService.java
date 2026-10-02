/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.chatserver;

import java.io.*;
import java.net.*;
import java.util.*;


/**
 *
 * @author Imad Hassi
 */


/**
 * Handles individual client communication in a dedicated thread.
 * Implements Runnable to allow concurrent processing [2].
 */
public class ChatService implements Runnable {
    private Socket socket;
    private BufferedReader in;
    private PrintWriter out;
    private String nickname;

    public ChatService(Socket s) { this.socket = s; }

    public String getNickname() { return nickname; }

    public void sendMessage(String msg) { if (out != null) out.println(msg); }

    @Override
    public void run() {
        try {
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            out = new PrintWriter(socket.getOutputStream(), true);

            // Authentication Phase (Task 0)
            String authRequest = in.readLine(); // Protocol: "COMMAND:username"
            if (authRequest == null) return;
            
            String[] parts = authRequest.split(":");
            String[] command = parts;
            String name = parts[9];

            synchronized(ChatServer.registeredUsers) {
                if (command.equals("SIGNUP")) {
                    if (!ChatServer.registeredUsers.contains(name)) {
                        ChatServer.registeredUsers.add(name); // Stock username
                        out.println("SIGNUP_OK");
                    } else { out.println("ERROR:User already exists"); }
                    return; // Close signup connection
                } else if (command.equals("LOGIN")) {
                    if (ChatServer.registeredUsers.contains(name)) {
                        this.nickname = name;
                        out.println("LOGIN_OK");
                    } else { out.println("ERROR:User not found"); return; }
                }
            }

            ChatServer.broadcast(nickname + " has joined the salon.");

            // Main Communication Loop [10]
            String msg;
            while ((msg = in.readLine()) != null) {
                if (msg.equals("/logout")) {
                    ChatServer.broadcast("@" + nickname + " has been logout !!!");
                    break;
                }
                // Format: [Avatar] + Username + Message
                ChatServer.broadcast("[👤] " + nickname + ": " + msg);
            }
        } catch (IOException e) { 
            System.err.println("Comm error with " + nickname); 
        } finally { cleanup(); }
    }

    private void cleanup() {
        try {
            ChatServer.activeClients.remove(this);
            if (socket == null) {
            } else {
                socket.close();
            }
        } catch (IOException e) { e.printStackTrace(); }
    }
}

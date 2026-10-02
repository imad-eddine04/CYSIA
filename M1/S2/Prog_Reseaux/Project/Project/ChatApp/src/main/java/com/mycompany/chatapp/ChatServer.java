/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */
package com.mycompany.chatapp;

import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.*;

/**
 *
 * @author Imad Hassi
 */
public class ChatServer {
    private static final int DEFAULT_PORT = 2000;
    private static Set<ClientHandler> clients = ConcurrentHashMap.newKeySet();
    private static Set<String> registeredUsers = ConcurrentHashMap.newKeySet();
    private static Set<String> onlineUsers = ConcurrentHashMap.newKeySet();
    private static Map<String, String> userAvatars = new ConcurrentHashMap<>();
    private static Map<String, byte[]> sharedFiles = new ConcurrentHashMap<>(); // fileName -> file data

    public static void main(String[] args) {
        // Load registered users from file
        loadRegisteredUsers();
        
        int port = args.length > 0 ? Integer.parseInt(args[0]) : DEFAULT_PORT;
        
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Chat Server started on port " + port);
            
            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("New client connected: " + clientSocket.getInetAddress());
                
                ClientHandler clientHandler = new ClientHandler(clientSocket);
                clients.add(clientHandler);
                new Thread(clientHandler).start();
            }
        } catch (IOException e) {
            System.err.println("Server exception: " + e.getMessage());
        }
    }
    
    private static void loadRegisteredUsers() {
        File usersFile = new File("users.txt");
        System.out.println("Loading users from: " + usersFile.getAbsolutePath());
        
        try (BufferedReader reader = new BufferedReader(new FileReader(usersFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String trimmedLine = line.trim();
                if (!trimmedLine.isEmpty()) {
                    String[] parts = trimmedLine.split(":");
                    if (parts.length >= 2) {
                        String username = parts[0].trim();
                        String avatar = parts[1].trim();
                        registeredUsers.add(username);
                        userAvatars.put(username, avatar);
                    } else if (parts.length == 1) {
                        // Handle old format without avatar
                        String username = parts[0].trim();
                        registeredUsers.add(username);
                        userAvatars.put(username, "😊"); // Default avatar
                    }
                }
            }
            System.out.println("Loaded " + registeredUsers.size() + " registered users: " + registeredUsers);
            System.out.println("User avatars: " + userAvatars);
        } catch (FileNotFoundException e) {
            System.out.println("No users file found at: " + usersFile.getAbsolutePath());
            System.out.println("Starting with empty user database. Users must sign up first.");
        } catch (IOException e) {
            System.err.println("Error loading users: " + e.getMessage());
        }
    }
    
    private static void reloadRegisteredUsers() {
        File usersFile = new File("users.txt");
        registeredUsers.clear();
        userAvatars.clear();
        
        try (BufferedReader reader = new BufferedReader(new FileReader(usersFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String trimmedLine = line.trim();
                if (!trimmedLine.isEmpty()) {
                    String[] parts = trimmedLine.split(":");
                    if (parts.length >= 2) {
                        String username = parts[0].trim();
                        String avatar = parts[1].trim();
                        registeredUsers.add(username);
                        userAvatars.put(username, avatar);
                    } else if (parts.length == 1) {
                        // Handle old format without avatar
                        String username = parts[0].trim();
                        registeredUsers.add(username);
                        userAvatars.put(username, "😊"); // Default avatar
                    }
                }
            }
            System.out.println("Reloaded " + registeredUsers.size() + " registered users: " + registeredUsers);
            System.out.println("User avatars: " + userAvatars);
        } catch (FileNotFoundException e) {
            System.out.println("No users file found during reload.");
        } catch (IOException e) {
            System.err.println("Error reloading users: " + e.getMessage());
        }
    }
    
    private static class ClientHandler implements Runnable {
        private Socket socket;
        private BufferedReader in;
        private PrintWriter out;
        private String username;
        private String avatar;
        
        public ClientHandler(Socket socket) {
            this.socket = socket;
        }
        
        @Override
        public void run() {
            try {
                in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                out = new PrintWriter(socket.getOutputStream(), true);
                
                // Handle login
                String loginMessage = in.readLine();
                System.out.println("Received login message: " + loginMessage);
                
                if (loginMessage != null && loginMessage.startsWith("LOGIN:")) {
                    username = loginMessage.substring(6).trim();
                    System.out.println("Attempting login for username: '" + username + "'");
                    
                    // Reload users to get latest signups
                    reloadRegisteredUsers();
                    System.out.println("Current registered users: " + registeredUsers);
                    
                    if (username.isEmpty()) {
                        System.out.println("Login failed: Empty username");
                        out.println("LOGIN_FAILED:Empty username");
                    } else if (!registeredUsers.contains(username)) {
                        System.out.println("Login failed: Username not registered - '" + username + "'");
                        out.println("LOGIN_FAILED:Username not registered. Please sign up first.");
                    } else if (onlineUsers.contains(username)) {
                        System.out.println("Login failed: Username already online - '" + username + "'");
                        out.println("LOGIN_FAILED:Username already logged in");
                    } else {
                        onlineUsers.add(username);
                        this.avatar = userAvatars.getOrDefault(username, "😊");
                        // If no avatar found, update the map with default
                        if (!userAvatars.containsKey(username)) {
                            userAvatars.put(username, "😊");
                        }
                        System.out.println("Login successful for: '" + username + "' with avatar: " + this.avatar);
                        out.println("LOGIN_OK:" + this.avatar);
                        broadcastMessage("SERVER:" + this.avatar + " " + username + " has joined the chat");
                        
                        // Handle chat messages
                        String message;
                        while ((message = in.readLine()) != null) {
                            if (message.equals("/logout")) {
                                break;
                            } else if (message.startsWith("COMMAND:LIST")) {
                                String userList = String.join(", ", onlineUsers);
                                out.println("RESPONSE:LIST:" + userList);
                            } else if (message.startsWith("COMMAND:NICK:")) {
                                String newUsername = message.substring(13).trim();
                                if (onlineUsers.contains(newUsername)) {
                                    out.println("RESPONSE:NICK:Username already taken");
                                } else {
                                    String oldUsername = username;
                                    onlineUsers.remove(username);
                                    onlineUsers.add(newUsername);
                                    userAvatars.put(newUsername, this.avatar);
                                    username = newUsername;
                                    out.println("RESPONSE:NICK:" + newUsername);
                                    broadcastMessage("SERVER:" + this.avatar + " " + oldUsername + " is now known as " + newUsername);
                                }
                            } else if (message.startsWith("COMMAND:AVAT:")) {
                                String newAvatar = message.substring(13).trim();
                                this.avatar = newAvatar;
                                userAvatars.put(username, newAvatar);
                                out.println("RESPONSE:AVAT:" + newAvatar);
                                broadcastMessage("SERVER:" + newAvatar + " " + username + " changed avatar");
                            } else if (message.startsWith("FILE:")) {
                                // Handle file upload
                                String[] fileInfo = message.substring(5).split(":");
                                if (fileInfo.length >= 2) {
                                    String fileName = fileInfo[0];
                                    String fileSize = fileInfo[1];
                                    broadcastMessage("FILE:" + this.avatar + " " + username + ":" + fileName + ":" + fileSize);
                                }
                            } else {
                                broadcastMessage(this.avatar + " " + username + ":" + message);
                            }
                        }
                    }
                } else {
                    System.out.println("Invalid login message format: " + loginMessage);
                    out.println("LOGIN_FAILED:Invalid login format");
                }
            } catch (IOException e) {
                System.err.println("Client handler exception: " + e.getMessage());
            } finally {
                cleanup();
            }
        }
        
        private void cleanup() {
            try {
                if (username != null) {
                    onlineUsers.remove(username);
                    broadcastMessage("SERVER:" + username + " has left the chat");
                }
                clients.remove(this);
                if (socket != null && !socket.isClosed()) {
                    socket.close();
                }
            } catch (IOException e) {
                System.err.println("Cleanup exception: " + e.getMessage());
            }
        }
        
        private void broadcastMessage(String message) {
            for (ClientHandler client : clients) {
                if (client != this && client.out != null) {
                    client.out.println(message);
                }
            }
        }
    }
}

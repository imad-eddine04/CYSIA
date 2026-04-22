/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/GUIForms/JFrame.java to edit this template
 */
package com.mycompany.chatapp;
import java.io.*;
import java.net.*;
import java.util.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.text.*;
import javax.swing.event.HyperlinkListener;
import javax.swing.event.HyperlinkEvent;
import javax.swing.JFileChooser;

/**
 *
 * @author Imad Hassi
 */
public class Chat extends javax.swing.JFrame {

    private Socket socket;
    private BufferedReader in;
    private PrintWriter out;
    private String username;
    private String avatar;
    private static List<String> messageHistory = new ArrayList<>();
    private static Map<String, String> pendingFiles = new HashMap<>(); // fileName -> sender
    private static String lastUploadedFile = null; // Track most recent file
    private static Map<String, File> storedFiles = new HashMap<>(); // fileName -> actual file

    /**
     * Creates new form Chat
     */
    public Chat() {
        initComponents();
    }

    Chat(Socket s, BufferedReader input, PrintWriter output, String user) {
        this(s, input, output, user, "😊"); // Default avatar
    }
    
    Chat(Socket s, BufferedReader input, PrintWriter output, String user, String avatar) {
        this.socket = s;
        this.in = input;
        this.out = output;
        this.username = user;
        this.avatar = avatar;
        initComponents();
        
        // Load message history
        for (String message : messageHistory) {
            chatArea.append(message + "\n");
        }
        
        // Make chat area untypable
        chatArea.setEditable(false);
        
        // Add ENTER key support for text field
        textField.addKeyListener(new KeyAdapter() {
            public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_ENTER) {
                    sendButtonActionPerformed(null);
                }
            }
        });

        // Background thread to read messages [8]
        new Thread(() -> {
            try {
                String line;
                while ((line = in.readLine()) != null) {
                    System.out.println("Received message: " + line);
                    if (line.startsWith("SERVER:")) {
                        String serverMsg = "[SERVER] " + line.substring(7);
                        chatArea.append(serverMsg + "\n");
                        messageHistory.add(serverMsg);
                    } else if (line.startsWith("RESPONSE:LIST:")) {
                        String userList = line.substring(14);
                        String listMsg = "Online users: " + userList;
                        chatArea.append(listMsg + "\n");
                        messageHistory.add(listMsg);
                    } else if (line.startsWith("RESPONSE:NICK:")) {
                        String newUsername = line.substring(14);
                        String nickMsg = "Your username changed to: " + newUsername;
                        chatArea.append(nickMsg + "\n");
                        messageHistory.add(nickMsg);
                        this.username = newUsername;
                    } else if (line.startsWith("RESPONSE:AVAT:")) {
                        String newAvatar = line.substring(14);
                        String avatMsg = "Your avatar changed to: " + newAvatar;
                        chatArea.append(avatMsg + "\n");
                        messageHistory.add(avatMsg);
                        this.avatar = newAvatar;
                    } else if (line.startsWith("FILE:")) {
                        // Handle file message
                        String fileData = line.substring(5);
                        String[] parts = fileData.split(":");
                        if (parts.length >= 3) {
                            String senderWithAvatar = parts[0];
                            String fileName = parts[1];
                            String fileSize = parts[2];
                            
                            // Extract sender name
                            String sender = senderWithAvatar;
                            if (senderWithAvatar.contains(" ")) {
                                int spaceIndex = senderWithAvatar.indexOf(' ');
                                sender = senderWithAvatar.substring(spaceIndex + 1);
                            }
                            
                            String fileMsg = senderWithAvatar + " sent file: " + fileName + " (" + fileSize + " bytes)";
                            chatArea.append(fileMsg + "\n");
                            messageHistory.add(fileMsg);
                            
                            // Add download instruction
                            String downloadMsg = "  Type: /download " + fileName + " to download\n";
                            chatArea.append(downloadMsg);
                            messageHistory.add(downloadMsg);
                            
                            // Store file info for download
                            pendingFiles.put(fileName, senderWithAvatar);
                            lastUploadedFile = fileName; // Track most recent file
                        }
                    } else {
                        int colonIndex = line.indexOf(':');
                        if (colonIndex > 0) {
                            String senderWithAvatar = line.substring(0, colonIndex);
                            String message = line.substring(colonIndex + 1);
                            
                            // Check if sender has avatar (format: "avatar username")
                            String sender;
                            if (senderWithAvatar.contains(" ")) {
                                int spaceIndex = senderWithAvatar.indexOf(' ');
                                sender = senderWithAvatar.substring(spaceIndex + 1);
                            } else {
                                sender = senderWithAvatar;
                            }
                            
                            String formattedMsg = senderWithAvatar + ": " + message;
                            chatArea.append(formattedMsg + "\n");
                            messageHistory.add(formattedMsg);
                        } else {
                            chatArea.append(line + "\n");
                            messageHistory.add(line);
                        }
                    }
                }
            } catch (IOException e) { 
                System.err.println("Connection lost: " + e.getMessage());
                chatArea.append("Connection lost.\n"); 
            }
        }).start();
    }
    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jScrollPane1 = new javax.swing.JScrollPane();
        chatArea = new javax.swing.JTextArea();
        textField = new javax.swing.JTextField();
        sendButton = new javax.swing.JButton();
        fileUpload = new javax.swing.JButton();
        logoutButton = new javax.swing.JButton();
        Download = new javax.swing.JButton();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        chatArea.setColumns(20);
        chatArea.setRows(5);
        jScrollPane1.setViewportView(chatArea);

        sendButton.setText("Send");
        sendButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                sendButtonActionPerformed(evt);
            }
        });

        fileUpload.setText("+");
        fileUpload.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                fileUploadActionPerformed(evt);
            }
        });

        logoutButton.setText("Logout");
        logoutButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                logoutButtonActionPerformed(evt);
            }
        });

        Download.setText("Download");

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                    .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 322, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addComponent(textField)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(sendButton)))
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(fileUpload, javax.swing.GroupLayout.PREFERRED_SIZE, 69, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(logoutButton)
                            .addComponent(Download, javax.swing.GroupLayout.PREFERRED_SIZE, 85, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addContainerGap())))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addGap(16, 16, 16)
                        .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 229, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED))
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(logoutButton)
                        .addGap(18, 18, 18)
                        .addComponent(Download)
                        .addGap(27, 27, 27)))
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(textField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(sendButton)
                    .addComponent(fileUpload))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void sendButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_sendButtonActionPerformed
        // TODO add your handling code here:
        String message = textField.getText().trim();
        if (!message.isEmpty() && out != null) {
            if (message.startsWith("/list")) {
                out.println("COMMAND:LIST");
            } else if (message.startsWith("/nick ")) {
                String newUsername = message.substring(6).trim();
                out.println("COMMAND:NICK:" + newUsername);
            } else if (message.startsWith("/avat ")) {
                String newAvatar = message.substring(6).trim().toLowerCase();
                String avatarSymbol = getAvatarSymbol(newAvatar);
                if (avatarSymbol != null) {
                    out.println("COMMAND:AVAT:" + avatarSymbol);
                } else {
                    chatArea.append("[SYSTEM] Invalid avatar. Use: happy, sad, AI, or ghost\n");
                }
            } else if (message.startsWith("/download ")) {
                String fileName = message.substring(10).trim();
                downloadFile(fileName);
            } else {
                out.println(this.avatar + " " + username + ":" + message);
                String formattedMsg = this.avatar + " " + username + ": " + message;
                chatArea.append(formattedMsg + "\n");
                messageHistory.add(formattedMsg);
            }
            textField.setText("");
        }
    }//GEN-LAST:event_sendButtonActionPerformed

    private void downloadFile(String fileName) {
        if (pendingFiles.containsKey(fileName)) {
            String sender = pendingFiles.get(fileName);
            chatArea.append("[SYSTEM] Downloading " + fileName + " from " + sender + "...\n");
            
            // Look for file in shared directory
            File sharedDir = new File("shared_files");
            File sourceFile = new File(sharedDir, fileName);
            
            if (sourceFile.exists()) {
                try {
                    File downloadDir = new File("downloads");
                    if (!downloadDir.exists()) {
                        downloadDir.mkdir();
                    }
                    
                    File destinationFile = new File(downloadDir, fileName);
                    
                    // Copy the file
                    try (FileInputStream fis = new FileInputStream(sourceFile);
                         FileOutputStream fos = new FileOutputStream(destinationFile)) {
                        
                        byte[] buffer = new byte[4096];
                        int bytesRead;
                        while ((bytesRead = fis.read(buffer)) > 0) {
                            fos.write(buffer, 0, bytesRead);
                        }
                    }
                    
                    chatArea.append("[SYSTEM] Download completed: " + fileName + "\n");
                    chatArea.append("[SYSTEM] File saved to: " + destinationFile.getAbsolutePath() + "\n");
                    
                } catch (IOException e) {
                    chatArea.append("[ERROR] Failed to download file: " + e.getMessage() + "\n");
                }
            } else {
                chatArea.append("[ERROR] File not found in shared directory: " + fileName + "\n");
            }
        } else {
            chatArea.append("[ERROR] File not found: " + fileName + "\n");
        }
    }

    private String getAvatarSymbol(String avatarName) {
        switch (avatarName) {
            case "happy":
                return "😊";
            case "sad":
                return "😢";
            case "ai":
                return "🤖";
            case "ghost":
                return "👻";
            default:
                return "User";
        }
    }

    private void logoutButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_logoutButtonActionPerformed
        // TODO add your handling code here:
        if (out != null) {
            out.println("/logout"); // Send logout protocol
        }
        new ChatApp().setVisible(true);
        this.dispose();
    }//GEN-LAST:event_logoutButtonActionPerformed

    private void fileUploadActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_fileUploadActionPerformed
        // TODO add your handling code here:
        JFileChooser fileChooser = new JFileChooser();
        int returnValue = fileChooser.showOpenDialog(this);
        if (returnValue == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            try {
                // Create shared files directory
                File sharedDir = new File("shared_files");
                if (!sharedDir.exists()) {
                    sharedDir.mkdir();
                }
                
                // Copy file to shared directory
                File sharedFile = new File(sharedDir, selectedFile.getName());
                try (FileInputStream fis = new FileInputStream(selectedFile);
                     FileOutputStream fos = new FileOutputStream(sharedFile)) {
                    
                    byte[] buffer = new byte[4096];
                    int bytesRead;
                    while ((bytesRead = fis.read(buffer)) > 0) {
                        fos.write(buffer, 0, bytesRead);
                    }
                }
                
                // Store the shared file reference
                storedFiles.put(selectedFile.getName(), sharedFile);
                
                // Send file info to server
                out.println("FILE:" + selectedFile.getName() + ":" + selectedFile.length());
                
                chatArea.append("[SYSTEM] File sent: " + selectedFile.getName() + "\n");
            } catch (IOException e) {
                chatArea.append("[ERROR] Failed to send file: " + e.getMessage() + "\n");
            }
        }
    }//GEN-LAST:event_fileUploadActionPerformed

    private void DownloadActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_DownloadActionPerformed
        // TODO add your handling code here:
        if (lastUploadedFile != null && pendingFiles.containsKey(lastUploadedFile)) {
            downloadFile(lastUploadedFile);
        } else {
            chatArea.append("[ERROR] No files to download!\n");
        }
    }//GEN-LAST:event_DownloadActionPerformed

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(Chat.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(Chat.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(Chat.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(Chat.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new Chat().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton Download;
    private javax.swing.JTextArea chatArea;
    private javax.swing.JButton fileUpload;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JButton logoutButton;
    private javax.swing.JButton sendButton;
    private javax.swing.JTextField textField;
    // End of variables declaration//GEN-END:variables
}

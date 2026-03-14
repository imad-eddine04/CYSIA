/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.mycompany.mavenproject1;

import java.net.*;


public class Mavenproject1 {

    public static void main(String[] args) {
       
        InetAddress adresse;
        try {
            adresse = InetAddress.getByName("www.facebook.com");
          
            System.out.println(adresse.getHostAddress());
        } catch (UnknownHostException e) {
        
    }
}
    }


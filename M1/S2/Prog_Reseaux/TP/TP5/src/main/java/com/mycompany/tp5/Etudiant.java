package com.mycompany.etudiant;

import java.io.Serializable;

public class Etudiant implements Serializable {

    private static final long serialVersionUID = 1L;

    private String nom;
    private String prenom;
    private int age;

    public Etudiant(String nom, String prenom, int age) {
        this.nom = nom;
        this.prenom = prenom;
        this.age = age;
    }

    public String getNom() {
        return nom;
    }

    @Override
    public String toString() {
        return "Etudiant : " + nom + " " + prenom + " est a " + age + " ans.";
    }
}
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import time
import os
import sqlite3


class Employe:
    def __init__(self, root):
        self.root = root
        self.root.title("Employe")
        self.root.geometry("1920x1040+0+0")
        self.root.config(bg="white")
        self.root.focus_force()

        self.var_num_fact = StringVar()
        self.facture_liste = []

        
        #Title 
        title = Label(self.root, text="Consulter la Facture des clients", font=("goudy old style",40,"bold"), bg="cyan", bd=3, relief=RIDGE).pack(side=TOP, fill=X, padx=10, pady=20)
        
        num_fact = Label(self.root, text="Numero Facture", font=("times new roman",25), bg="white").place(x=50, y=105)
        ecri_num_fact = Entry(self.root, textvariable=self.var_num_fact, font=("times new roman",20), bg="lightyellow").place(x=270, y=110, width=200)

        #Bouton recherche et tous
        btn_recherche = Button(self.root, command=self.recherche, text="Recherche", font=("times new roman",15, "bold"), cursor="hand2", bg="green",fg="white").place(x=480, y=110, width=180, height=40)
        btn_renit = Button(self.root, command=self.effacer, text="Reinitialiser", font=("times new roman",15, "bold"), cursor="hand2", bg="lightgray").place(x=670, y=110, width=180, height=40)

        #Liste Facture Vendu
        vente_frame = Frame(self.root, bd=3, relief=RIDGE)
        vente_frame.place(x=10, y=170, width=300, height=460)
        
        scroll_y = Scrollbar(vente_frame, orient=VERTICAL)
        self.list_vente = Listbox(vente_frame, font=("goudy old style", 15), bg="white", yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.list_vente.yview)
        self.list_vente.pack(fill=BOTH, expand=1)

        self.list_vente.bind("<ButtonRelease-1>", self.recuper_donnees)

        
        #espace Facture 
        facture_frame = Frame(self.root, bd=3, relief=RIDGE)
        facture_frame.place(x=320, y=170, width=550, height=460)

        title = Label(facture_frame, text="Facture du client", font=("goudy old style",20,"bold"), bg="orange").pack(side=TOP, fill=X)

        scroll_y2 = Scrollbar(facture_frame, orient=VERTICAL)
        self.espace_facture = Text(facture_frame, font=("goudy old style", 12), bg="lightyellow", yscrollcommand=scroll_y2.set)
        scroll_y2.pack(side=RIGHT, fill=Y)
        scroll_y2.config(command=self.espace_facture.yview)
        self.espace_facture.pack(fill=BOTH, expand=1)

        #image
        self.facture_photo = Image.open(r"C:\Users\HP\Desktop\Python_Projects\gestion_magasin\image\cat2.jpg")
        self.facture_photo = self.facture_photo.resize((390,530))
        self.facture_photo = ImageTk.PhotoImage(self.facture_photo)

        label_image = Label(self.root, image=self.facture_photo)
        label_image.place(x=870, y=100)

        self.affiche_resultat()

        #Fonctions
    def affiche_resultat(self):
        del self.facture_liste[:]
        self.list_vente.delete(0, END)

        for i in os.listdir(r"C:\Users\HP\Desktop\Python_Projects\gestion_magasin\facture"):
            if i.split(".")[-1] == "txt":
                self.list_vente.insert(END, i)
                self.facture_liste.append(i.split(".")[0])

    def recuper_donnees(self, ev):
        index_ = self.list_vente.curselection()
        nom_fichier = self.list_vente.get(index_)
        fichier_ouvert = open(fr"C:\Users\HP\Desktop\Python_Projects\gestion_magasin\facture\{nom_fichier}", "r")
        self.espace_facture.delete("1.0", END)
        for i in fichier_ouvert:
            self.espace_facture.insert(END, i)
        fichier_ouvert.close()


    def recherche(self):
            if self.var_num_fact.get()=="":
                messagebox.showerror("Erreur", "Donner un numero de facture")
            else:
                
                if self.var_num_fact.get() in self.facture_liste:
                    fichier_ouvert = open(fr"C:\Users\HP\Desktop\Python_Projects\gestion_magasin\facture\{self.var_num_fact.get()}.txt", "r")
                    self.espace_facture.delete("1.0", END)
                    for i in fichier_ouvert:
                        self.espace_facture.insert(END, i)
                    fichier_ouvert.close()
                else:
                    messagebox.showerror("Erreur", "Numero de facture invalide !")


    def effacer(self):
        self.affiche_resultat()
        self.espace_facture.delete("1.0", END)
        self.var_num_fact.set("")
        




if __name__=="__main__":
    root = Tk()
    obj = Employe(root)
    root.mainloop()
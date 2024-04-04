from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import os
import smtplib
import email_password
import time

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Connexion")
        self.root.geometry("1920x1040+0+0")
        self.root.config(bg="white")
        self.root.focus_force()

        self.code_envoie = ""

        login_frame = Frame(self.root, bg="cyan")
        login_frame.place(x=380, y=90, width=500, height=500)

        #Title 
        title = Label(login_frame, text="Connexion", font=("algerian",40,"bold"), bg="cyan", fg="black")
        title.pack(side=TOP, fill=X)

        #ID Employe
        id = Label(login_frame, text="ID Employe", font=("times new roman",30,"bold"), bg="cyan").place(x=150, y=100)
        self.ecri_id = Entry(login_frame, font=("times new roman",20), bg="lightgrey")
        self.ecri_id.place(x=100, y=160)
        #password
        password = Label(login_frame, text="Password", font=("times new roman",30,"bold"), bg="cyan").place(x=150, y=200)
        self.ecri_password = Entry(login_frame, show="*", font=("times new roman",20), bg="lightgrey")
        self.ecri_password.place(x=100, y=270)

        # Les boutons de validation et connexion
        connexion_btn = Button(login_frame, text="Connexion", command=self.connexion, cursor="hand2", font=("times new roman",20,"bold"), bg="lightgray", fg="green").place(x=180, y=320)
        oubli_btn = Button(login_frame, text="Mot de passe oublie", command=self.password_oublie_fenetre, cursor="hand2", font=("times new roman",15), bd=0, bg="cyan", fg="red", activebackground="cyan").place(x=180, y=450)

   
    def connexion(self):
        if self.ecri_id.get()=="" or self.ecri_password.get()=="":
            messagebox.showerror("Erreur", "Veuillez donner votre ID employe et mot de passe !", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database=r"C:/Users/HP/Desktop/Python_Projects/gestion_magasin/Donnee/magasinbase.db")
                cur = con.cursor()
                cur.execute("SELECT type FROM employe WHERE eid=? AND password=?", (self.ecri_id.get(), self.ecri_password.get()) )
                user = cur.fetchone()
                if user == None:
                    messagebox.showerror("Erreur", "L'ID Employe/Mot de passe n'existe pas !", parent=self.root)
                else:
                    if user[0] == 'Admin':
                        self.root.destroy()
                        os.system("C:/Users/HP/Desktop/Python_Projects/gestion_magasin/accueil.py")
                    else:
                        self.root.destroy()
                        os.system("C:/Users/HP/Desktop/Python_Projects/gestion_magasin/caisse.py")
            except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !", parent=self.root)


    
    def password_oublie_fenetre(self):
        if  self.ecri_id.get()=="":
            messagebox.showerror("Erreur","Veuillez saisir votre ID Employe !", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database=r"C:/Users/HP/Desktop/Python_Projects/gestion_magasin/Donnee/magasinbase.db")
                cur = con.cursor()
                
                cur.execute("select email from employe where eid=?", self.ecri_id.get())
                mail = cur.fetchone()
                if mail == None: 
                    messagebox.showerror("Erreur","L'ID Employe est invalide !", parent=self.root)
                else:    
                    check = self.envoie_mail(mail[0])  
                    if check == "f":
                        messagebox.showerror("Erreur","Veuillez verifier votre connexion", parent=self.root)
                    else:
                        self.var_code = StringVar()
                        self.var_new_pass = StringVar()
                        self.var_conf_pass = StringVar()
                        self.root2 = Toplevel()
                        self.root2.title("Reinitialiser mot de passe")
                        self.root2.geometry("400x400+800+500")
                        self.root2.config(bg="white")
                        self.root2.focus_force()
                        self.root2.grab_set()

                        #Title 
                        title = Label(self.root2, text="Mot de passe oublie", font=("algerian",20,"bold"), bg="red").pack(side=TOP, fill=X)

                        #Code
                        code = Label(self.root2, text="Saisir le code recu par mail", font=("times new roman",15,"bold"), bg="white").place(x=70, y=50)
                        ecri_code = Entry(self.root2, textvariable=self.var_code, font=("times new roman",15), bg="lightgrey").place(x=70, y=100, width=200)

                        #Bouton changer mot de passe
                        self.code_btn = Button(self.root2, text="Valider", command=self.code_valide, cursor="hand2", font=("times new roman",15,"bold"), bg="green", fg="black")
                        self.code_btn.place(x=300, y=90)
                        
                        #Nouveau mot de passe
                        new_password = Label(self.root2, text="Nouveau mot de passe", font=("times new roman",15,"bold"), bg="white").place(x=70, y=150)
                        ecri_new_password = Entry(self.root2, textvariable=self.var_new_pass, show="*", font=("times new roman",15), bg="lightgrey").place(x=70, y=200, width=250)

                        #Confirme mot de passe
                        confirm_password = Label(self.root2, text="Confirme mot de passe", font=("times new roman",15,"bold"), bg="white").place(x=70, y=250)
                        ecri_confirm_password= Entry(self.root2, textvariable=self.var_conf_pass, show="*", font=("times new roman",15), bg="lightgrey").place(x=70, y=300, width=250)

                        #Bouton changer mot de passe
                        self.modifier_btn = Button(self.root2, text="Moifier", command=self.modifier, cursor="hand2", state=DISABLED, font=("times new roman",15,"bold"), bg="yellow")
                        self.modifier_btn.place(x=160, y=350)


            except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !", parent=self.root)


    def reini(self):
        self.ecri_question.delete(0, END),
        self.ecri_reponse.delete(0, END),
        self.ecri_new_password.delete(0, END)

    def modifier(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Erreur","Veuillew saisir votre nouveau mot de passe")
        elif self.var_new_pass.get() != self.var_conf_pass.get():
            messagebox.showerror("Erreur","Le nouveau mot de passe et confirme mot de passe doivent etre identiques")
        else:
            try:
                con = sqlite3.connect(database=r"C:/Users/HP/Desktop/Python_Projects/gestion_magasin/Donnee/magasinbase.db")
                cur = con.cursor()
                
                cur.execute("update  employe set password=? where eid=?", (self.var_new_pass.get(), self.ecri_id.get()) )
                con.commit()
                messagebox.showinfo("Succes", "Vous avez modifie votre mot de passe !", parent=self.root2)
                self.root2.destroy()

            except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !", parent=self.root2)



    #Envoie du code par mail
    def envoie_mail(self, to_):
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        email_ = email_password.email_
        password_ = email_password.password_

        s.login(email_, password_)

        self.code_envoie = int(time.strftime("%H%M%S")) + int(time.strftime("%S"))

        subj = "Magasin Hamza Barka Code de reinitialisation"
        sms = f"Bonjour Monsieur/Madame \n\nvotre code de reinitialisation est : {self.code_envoie} \n\nMerci d'avoir utiliser notre service !"
        message = "Subject : {}\n\n{}".format(subj, sms)
        s.sendmail(email_, to_, message)

        check = s.ehlo()
        if check[0] == 250:
            return 's'
        else:
            return 'f'
        


    #Verification du code
    def code_valide(self):
        if int(self.code_envoie) == int(self.var_code.get()):
            self.modifier_btn.config(state=NORMAL)
            self.code_btn.config(state=DISABLED)
        else:
            messagebox.showerror("Erreur","Code valide")


root = Tk()
obj = Login(root)
root.mainloop()
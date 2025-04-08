from tkinter import *
import sqlite3

# Interface graphique:
fenetre = Tk()
fenetre.title('TNSI_Bouklikha_Mohamed-Amine_jeu_MesMusiques')
fenetre.config(width=950, height=600)

# Connexion à la base de données
connexion = sqlite3.connect("MesMusiques.db")
curseur = connexion.cursor()

# Fonction de recherche par auteur
def recherche_auteur():
    '''récupérer les informations de l'auteur et des morceaux associés. Si aucun
    résultat n'est trouvé, elle affiche un message indiquant que l'auteur n'existe pas.'''
    nom_auteur = entry_recherche_nom.get()
    curseur.execute("""SELECT Auteur.nom, Auteur.prenom, Auteur.style_musique, Auteur.naissance, Morceaux.titre
                       FROM Auteur
                       JOIN Morceaux ON Auteur.id_auteur = Morceaux.id_auteur
                       WHERE Auteur.nom = ?""", (nom_auteur,))
    resultats = curseur.fetchall()
    if not resultats:
        affichage_resultat.config(text="L'auteur n'existe pas.")
        return
    affichage_resultat.config(text="")  # Effacer le contenu précédent
    for ligne in resultats:
        affichage_resultat.config(text=affichage_resultat.cget("text") + "Nom: " + ligne[0] + ", Prénom: " + ligne[1] + ", Style: " + ligne[2] + ", Naissance: " + str(ligne[3]) + ", Morceau: " + ligne[4] +"\n")

def ajouter_auteur():
    '''récupère les détails de l'auteur à partir des champs d'entrée de l'interface utilisateur,
    vérifie s'il n'existe pas déjà dans la base de données, puis l'ajoute si c'est le cas.'''
    nom = entry_nom.get()
    prenom = entry_prenom.get()
    style = entry_style.get()
    naissance = entry_naissance.get()

    # Vérifie si l'auteur existe déjà en spécifiant explicitement les colonnes dans SELECT
    curseur.execute("SELECT nom, prenom, style_musique, naissance FROM Auteur WHERE nom = ? AND prenom = ? AND style_musique = ? AND naissance = ?", (nom, prenom, style, naissance))
    resultats = curseur.fetchall()
    if not resultats:
        curseur.execute("INSERT INTO Auteur (nom, prenom, style_musique, naissance) VALUES (?, ?, ?, ?)", (nom, prenom, style, naissance))
        connexion.commit()
        affichage_resultat.config(text="Auteur ajouté avec succès.\n")
    else:
        affichage_resultat.config(text="L'auteur existe déjà.\n")

def supprimer_auteur():
    '''recherche l'auteur en fonction du nom spécifié, récupère son identifiant,
    puis supprime tous les morceaux associés à cet auteur et l'auteur lui-même.'''
    nom_auteur = entry_recherche_nom.get()
    # Récupérer l'ID de l'auteur basé sur le nom
    curseur.execute("SELECT id_auteur FROM Auteur WHERE nom = ?", (nom_auteur,))
    id_auteur = curseur.fetchone()
    if id_auteur:
        # Supprimer tous les morceaux associés à cet auteur
        curseur.execute("DELETE FROM Morceaux WHERE id_auteur = ?", (id_auteur[0],))
        # Puis, supprimer l'auteur lui-même
        curseur.execute("DELETE FROM Auteur WHERE id_auteur = ?", (id_auteur[0],))
        connexion.commit()
        affichage_resultat.config(text="L'auteur et tous ses morceaux ont été supprimés.")
    else:
        affichage_resultat.config(text="L'auteur n'existe pas.")

def recherche_morceau():
    '''rechercher le morceau par son titre, récupère les informations sur l'auteur
    associé, puis affiche les détails du morceau.'''
    titre_morceau = entry_recherche_nom.get()
    curseur.execute("""SELECT Auteur.nom, Auteur.prenom, Morceaux.titre, Morceaux.annee_sortie
                       FROM Morceaux
                       JOIN Auteur ON Morceaux.id_auteur = Auteur.id_auteur
                       WHERE Morceaux.titre = ?""", (titre_morceau,))
    resultats = curseur.fetchall()
    if not resultats:
        affichage_resultat.config(text="Le morceau n'existe pas.")
        return
    affichage_resultat.config(text="")  # Effacer le contenu précédent
    for ligne in resultats:
        affichage_resultat.config(text=affichage_resultat.cget("text") + "Auteur: " + ligne[0] + " " + ligne[1] + ", Titre: " + ligne[2] + ", Année: " + str(ligne[3]) + "\n")


def ajouter_morceau():
    '''récupère les détails du morceau à partir des champs d'entrée de l'interface utilisateur,
    vérifie si l'auteur associé existe, puis ajoute le morceau à la base de données.'''
    titre = entry_titre.get()
    annee_sortie = entry_annee.get()
    nom_auteur = entry_auteur.get()

    # Vérifie si l'auteur existe déjà, en spécifiant explicitement la colonne qui nous intéresse
    curseur.execute("SELECT id_auteur FROM Auteur WHERE nom = ?", (nom_auteur,))
    resultats = curseur.fetchall()
    if not resultats:
        affichage_resultat.config(text="L'auteur n'existe pas. Veuillez l'ajouter d'abord.\n")
        return
    else:
        id_auteur = resultats[0][0]  # Récupérer l'ID de l'auteur existant

    # Insérer le morceau
    curseur.execute("INSERT INTO Morceaux (titre, annee_sortie, id_auteur) VALUES (?, ?, ?)", (titre, annee_sortie, id_auteur))
    connexion.commit()
    affichage_resultat.config(text="Morceau ajouté avec succès.\n")

def supprimer_morceau():
    '''recherche le morceau en fonction du titre spécifié, puis le supprime s'il existe.'''
    titre_morceau = entry_recherche_nom.get()
    # Vérifier d'abord si le morceau existe
    curseur.execute("SELECT titre FROM Morceaux WHERE titre = ?", (titre_morceau,))
    resultat = curseur.fetchone()

    if resultat:
        # Supprimer le morceau s'il existe
        curseur.execute("DELETE FROM Morceaux WHERE titre = ?", (titre_morceau,))
        connexion.commit()
        affichage_resultat.config(text="Le morceau a été supprimé.")
    else:
        affichage_resultat.config(text="Le morceau n'existe pas.")



#Boutons et Entree

recherche_text = Label(fenetre, text="RECHERCHE PAR NOM",font=('arial',12,'bold'),bg='blue')
recherche_text.place(x=10,y=20)

entry_recherche_nom = Entry(fenetre)
entry_recherche_nom.place(x=10,y=60)

btn_recherche_auteur = Button(fenetre, text="Chercher l'Auteur", command=recherche_auteur)
btn_recherche_auteur.place(x=10,y=85)

btn_recherche_morceau = Button(fenetre, text="Chercher le Morceau", command=recherche_morceau)
btn_recherche_morceau.place(x=10,y=125)

btn_supprimer_auteur = Button(fenetre, text="Supprimer Auteur", command=supprimer_auteur)
btn_supprimer_auteur.place(x=160, y=85)

btn_supprimer_morceau = Button(fenetre, text="Supprimer Morceau", command=supprimer_morceau)
btn_supprimer_morceau.place(x=160, y=125)



ajoute_text = Label(fenetre, text="AJOUTER ",font=('arial',12,'bold'),bg='yellow')
ajoute_text.place(x=10,y=170)

auteur_text = Label(fenetre, text="Auteur ",font=('arial',10,'bold'))
auteur_text.place(x=50,y=210)

entry_nom = Entry(fenetre)
entry_nom.place(x=10,y=240)

entry_prenom = Entry(fenetre)
entry_prenom.place(x=10,y=270)

entry_style = Entry(fenetre)
entry_style.place(x=10,y=300)

entry_naissance = Entry(fenetre)
entry_naissance.place(x=10,y=330)

nom_aut_text = Label(fenetre, text=":    Nom",font=('arial',8,'bold'))
nom_aut_text.place(x=150,y=240)

prenom_aut_text = Label(fenetre, text=":    Prénom",font=('arial',8,'bold'))
prenom_aut_text.place(x=150,y=270)

style_aut_text = Label(fenetre, text=":    Style De Musique",font=('arial',8,'bold'))
style_aut_text.place(x=150,y=300)

naissance_aut_text = Label(fenetre, text=":    Année De Naissance",font=('arial',8,'bold'))
naissance_aut_text.place(x=150,y=330)

btn_ajoute = Button(fenetre, text="Ajoute Auteur", command=ajouter_auteur)
btn_ajoute.place(x=30,y=360)


morceaux_text = Label(fenetre, text="Morceaux ",font=('arial',10,'bold'))
morceaux_text.place(x=40,y=410)

entry_titre= Entry(fenetre)
entry_titre.place(x=10,y=440)

entry_annee = Entry(fenetre)
entry_annee.place(x=10,y=470)

entry_auteur = Entry(fenetre)
entry_auteur.place(x=10,y=500)

titre_mor_text = Label(fenetre, text=":    Titre",font=('arial',8,'bold'))
titre_mor_text.place(x=150,y=440)

annee_mor_text = Label(fenetre, text=":    Année De Sortie",font=('arial',8,'bold'))
annee_mor_text.place(x=150,y=470)

auteur_mor_text = Label(fenetre, text=":    Auteur",font=('arial',8,'bold'))
auteur_mor_text.place(x=150,y=500)

btn_morceaux = Button(fenetre, text="Ajoute Morceaux",command=ajouter_morceau)
btn_morceaux.place(x=20,y=530)




consigne = Label(fenetre, text="➠ Pour faire une recherche taper le nom de l'auteur ou du morceaux désiré\n "
                               "➠ Pour ajouter un morceaux il faut que l'auteur existe dans la base de donnée afin de le préciser \n"
                               "➠ Pour rechercher un auteur ou morceaux que vous avez ajouter il faut avoir\n bien renter toutes les infos dessus\n"
                               "➠ Pour supprimer il suffit de noter le nom de l'auteur ou du morceaux ",font=('arial',8,'bold'))
consigne.place(x=320,y=470)

affichage_resultat = Label(fenetre, width=80, height=30,fg='black',bg='beige',font=('arial',8,'bold'))
affichage_resultat.place(x=320,y=20)

fenetre.mainloop()

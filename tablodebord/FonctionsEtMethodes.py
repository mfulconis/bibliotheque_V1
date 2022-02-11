import sqlite3
from datetime import datetime
import os
from django.conf import settings

# Fonction pour définir la date du jour


def DateDuJour():
    maintenant = datetime.now()
    maintenant = str(maintenant.day) + '-' + str(maintenant.month) + '-' + str(maintenant.year)
    return maintenant

# Fonctions remplacement caractères


def SuprCar(chaine):
    carspe = "'${[()]}"
    for c in carspe:
        locals()
        chaine = chaine.replace(c,'')
    return chaine

# Fonctions du menu principal


def quitter():
    quit()

# Verifier si l'auteur existe dans a table auteur../db.sqlite3


def verifier(var):
    conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'db.sqlite3'))
    cur = conn.cursor()
    cur.execute('SELECT id, nom FROM tablodebord_auteur WHERE nom = ?', (str(var),))
    cur = cur.fetchone()
    conn.commit()
    conn.close()
    print(cur)
    return cur

# Supprimer les enregistrement de la base de données


def  SupprimerEnregistrement():
    conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'db.sqlite3'))
    cur = conn.cursor()
    cur.execute("DELETE FROM tablodebord_auteur;")
    cur.execute("DELETE FROM tablodebord_livre;")
    cur.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'tablodebord_auteur';")
    cur.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'tablodebord_livre';")
    #cur.execute('DELETE FROM sqlite_sequence WHERE name=‘tablodebord_livre‘;')
    conn.commit()
    conn.close()
    return

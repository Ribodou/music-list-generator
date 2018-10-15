# -*- coding: utf-8 -*-

# Copyright (C) 2017 Lucas Robidou
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# PS: For any question or any suggestion, please contact me at:
#luc.robidou@gmail.com

# but du programme:
# creer une base de donnée contenant toutes les musiques d'un repertoire

#goal: create a database which contains every music in a directory.


# ----- import des modules necessaire ----------------------------------
import os.path 
import sqlite3
import sys
args = sys.argv

DEFAULT_DIRECTORY = "/home/lucas/Musique"
# ----- definition des fonctions ---------------------------------------
def creation(liste_comande):
    """
    but: creer une base de donnée à partir de la liste des commandes
    entree: liste
    sortie: rien
    """
    #creation
    fichiermusique ="/home/lucas/Musique/musique.sq3"#change username
    conn =sqlite3.connect(fichiermusique)
    cur =conn.cursor()
    cur.execute("CREATE TABLE musique (clefmusique INTEGER PRIMARY KEY,\
     chemin TEXT, temps REAL)")
    
    #remplissage
    for commande in liste_comande:
        print(commande)
        cur.execute(commande)
    conn.commit()
    
    #fermeture
    cur.close()
    conn.close()

def listdirectory(path):
    """
    but: lister tout les fichier du repertoire
    entree: chaine de caractere
    sortie: liste
    """ 
    fichier=[]  
    for root, dirs, files in os.walk(path):  
        for i in files:  
            fichier.append(os.path.join(root, i))  
    return fichier

# ----- corps du programme principal -----------------------------------
# you should change this line if your name is different
if (len(args) == 2):
	liste = listdirectory(args[1])
else:	
	liste = listdirectory(DEFAULT_DIRECTORY)
liste_comande = []

for musique in liste:
    if not "'" in musique:
        #"/home/user/musique/x.ogg" -> ["home","user","musique","x.ogg"]
        chemin = musique.split('/')
        try:
            titre = chemin[-1].split('.')
            if titre[1] == 'ogg' or titre[1] == 'mp3':
                temps = os.popen("mediainfo --Inform=\"General;%Duration%\"" + " " + "\""+ musique + "\"").read()
                temps = float(temps)/1000/60
                temps = round(temps*100)/100
                commande = "INSERT INTO musique(chemin,temps) VALUES(" + "'" + musique + "'," + str(temps) + ")"
                liste_comande.append(commande)
        except:
            pass
print("ok")
creation(liste_comande)

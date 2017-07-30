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

#But : Jouer à "le compte est bon" avec des temps de musiques
#      pour jouer des musiques autant de temps que le temps voulu
#      sans avoir à couper une musique.



#----- import des modules -----
import time
date_depart = time.time()
from itertools import combinations
from random import randrange
import numpy as np
import sqlite3
import os
from math import factorial
import os

#----- fonctions -------------------------------------------------------
date_import = time.time()-date_depart

#determination du nombre maximun d'element "prenable"
def determination_maxi(liste, but):
    """
    goal: find how many music you can take
    input: list, integer
    output: integer
    """
    somme = liste[0]
    i = 0
    while(somme<but) and i<len(liste):
        i = i+1
        somme += liste[i]
    return(i+1)

#determination du nombre minimun d'element "prenable"
def determination_mini(liste, but):
    """
    goal: find how many music you must take
    input: list, integer
    output: integer
    """
    taille = len(liste)
    somme = liste[taille-1]
    i = taille-1
    while(somme<but)and i<len(liste):
        i = i-1
        somme += liste[i]
    return(taille - i)

def somme_tuple(tuple_a_sommer):
    """
    goal: find he sum of all the element of a tuple
    input: tuple
    output: integer
    """
    somme = 0
    for element in tuple_a_sommer:
        somme += element
    return(somme)

def minute_vers_base_dix(nombre):
    """
    goal: turn an integer from base 60 to base 10 ("10.30 -> 10.5")
    input: float
    output: float
    """  
    nombre = str(  float(nombre)  )
    nombres = nombre.split(".")
    if len(nombres[1]) == 1:
        nombres[1] = nombres[1] + "0"
    nombres[1] = float(nombres[1])
    nombres[1] = (nombres[1] / 60)
    nombre = float(nombres[0]) + nombres[1]
    return round(nombre,2)

def consultation():
    """
    goal: find path and time of all the musique in the database
    input: nothing
    output: tuple of list
    """
    les_chemins = []
    les_temps = []
    conn =sqlite3.connect("/home/lucas/Musique/musique.sq3")
    cur =conn.cursor()
    cur.execute("SELECT chemin, temps FROM musique LIMIT 250")
    rows = cur.fetchall()
    #rows: list of tuple like ('/home/user/path/music.extension','12.65')
    for row in rows:
        les_temps.append(row[1])
        les_chemins.append(row[0])
    cur.close()
    conn.close()
    return(les_chemins, les_temps)



#----- corps du programme principal ------------------------------------
commande = "mplayer"#commande linux


#here is the time you have to change
but = 6.40



but = minute_vers_base_dix(but)

time_list = []#liste des temps des musiques
path_list = []#liste des chemins des musiques
(path_list, time_list) = consultation()
indices = []#listes des indices des musiques

#on convertit les minutes en base 10 et on construit la liste indices
for i in range(len(time_list)):
	time_list[i] = minute_vers_base_dix(time_list[i])
	indices.append(i)

#ces elements bornent les recherches: de plus, si l'on veut min ou max
#element, on prendra les min derniers ou les max premiers
nb_element_max = determination_maxi(time_list, but)
nb_element_min = determination_mini(time_list, but) - 1

combinaison_temps = []
combinaison_indices = []
difference = []


for nbelement in range(nb_element_min, nb_element_max+1):
	combinaison_temps.append(list(combinations(time_list,nbelement)))
	combinaison_indices.append(list(combinations(indices,nbelement)))
    
date_melange = time.time()-date_depart

for longueur in combinaison_temps:
	for element in longueur:
		somme = somme_tuple(element)
		#Seul l'ecart en valeur absolue par raport au but est interessant.
		difference.append(abs(somme-but))
liste_combinaison_indice = []
for longueur in combinaison_indices:
	for element in longueur:
		liste_combinaison_indice.append(element)



#A ce stade, on a:
#1)liste_indices: une liste de tuple d'indices
#2)liste_temps: une liste de tuple de temps : liste_indices[x][y] est de plus la musique qui dure liste_temps[x][y] minutes
#3)difference: une liste de float, chaque elemeent representant la somme des nombres contenu dans les float de liste_temps moins le but


indice_choix = []

indice_mini = difference.index(min(difference))
indice_choix.append(indice_mini)
difference.pop(indice_mini)


indice_tuple_final = indice_choix[randrange(len(indice_choix))]
tuple_final = liste_combinaison_indice[indice_tuple_final]


#vérification de la durée
duree = 0
for i in tuple_final:
	duree += time_list[i]

#on complete la commande
for element  in tuple_final:
	commande += " \""
	commande += path_list[element]
	commande += "\""


#print(commande)
os.system(commande)

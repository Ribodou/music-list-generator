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

# ----- notations ------------------------------------------------------
# On appele "chemin" une facon de jouer des musiques (=liste d'indice de musique)

#deter mini a refaire?

#----- import des modules ----------------------------------------------
import numpy as np
import random as rd
import time
import matplotlib.pyplot as plt
import sqlite3
import time
import os

# ----- definition des fonctions ---------------------------------------
deb = time.time()
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
    return i

#determination du nombre minimun d'element "prenable" A REFAIRE
def determination_mini(liste, but):
    """
    goal: find how many music you must take
    input: list, integer
    output: integer
    """
    taille = len(liste)
    somme = liste[-1]
    i = -1
    while(somme<but)and i<len(liste):
        i = i-1
        somme += liste[i]
    return abs(i)

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
    cur.execute("SELECT chemin, temps FROM musique WHERE temps > 2 AND temps < 6 ORDER BY temps ASC")
    rows = cur.fetchall()
    #rows: list of tuple like ('/home/user/path/music.extension','12.65')
    for row in rows:
        les_temps.append(row[1])
        les_chemins.append(row[0])
    cur.close()
    conn.close()
    #print(len(les_temps))
    return(les_chemins, les_temps)





# ----- partie AG ------------------------------------------------------
def normaliser(chemin, n) :
    """
    but: creer un chemin valide de taille n
    entree: liste, entier
    sortie: liste
    """
    normal = []
    for elem in chemin :
        if elem not in normal :
            normal.append(elem)
    # on complete
    while len(normal) < n:
        i = rd.randint(0,len(les_chemins)-1)
        if i not in normal:
            normal.append(i)
    return normal

def creer_population(taille,n):
    """
    but: creer une population alaeatoire qui soit compatible avec le problème
    entree: entier, entier
    sortie: list de liste
    """
    population = []
    L = [i for i in range(len(les_chemins)-1)]#liste des points
    for i in range(taille):
        N = L[:]
        chemin = []
        #chemin.append([0,0])
        while len(chemin) < n:
            i = rd.randint(0,len(les_chemins)-1)
            if i not in chemin:
                chemin.append(i)
        population.append((chemin, score_chemin(chemin)))
    #population = np.array(population)
    
    return population

def score_chemin(chemin) :
    """
    but: calculer la longueur d'un chemin
    entree: liste, liste de liste
    sortie: entier
    """
    temps = 0
    for element in chemin:
        temps += les_temps[element]
    return abs(temps-but)

def reduire(p):
    """
    but: reduire la population de moitiée en supprimant les moins bons elements
    entree: liste
    sortie: rien
    """
    ordre = []
    for e in p:
        ordre.append(e[1])
    arg = np.array(ordre).argsort()
    p_tri = p[:]
    #on "vide" p
    for i in range(len(p)):
        p.pop(0)
    for e in arg[:len(arg)//2]:
        p.append(p_tri[e])

def muter_chemin(chemin_a_muter):
    """
    but: introduire un element aleatoire dans une liste
    entree: liste
    sorite: rien
    """
    i = rd.randint(0,len(chemin_a_muter)-1)
    chemin_a_muter[i] = rd.randint(0,len(les_chemins)-1)

def muter_population(p,proba):
    """
    but: changer un element d'un element d'une liste avec une
    probabilité "proba" (loi de probabilité uniforme)
    entree: liste, entier, liste de liste
    sortie: rien
    """
    for i in range(len(p)//10,len(p)):
        if rd.random()<(1-np.exp(-i/600)):
            muter_chemin(p[i][0])
            p[i] = p[i][0],score_chemin(p[i][0])

def croiser(c1, c2,n):
    """
    but: creer, à partir de deux individus, uun troisième individus, qui
    soit conforme au problème
    entree: liste, liste
    sortie: liste
    """
    c = []
    for i in range(len(c1)//2):
        c.append(c1[i])
    for i in range(len(c2)//2,len(c2)):
        c.append(c2[i])
    c = normaliser(c,n)
    return c

def nouvelle_generation(p,n):
    """
    but: reconstituer une nouvelle génération avec des mutations des
    individus restants (chaque individus mute avec son voisin)
    entree: entier, liste de liste
    sortie: rien
    """
    for i in range(-1,len(p)):
        croisement = croiser(p[i][0],p[i+1][0],n)
        p.append((croisement,score_chemin(croisement)))

def algo_genetique(taille,n,proba):
    pop = creer_population(taille,n)
    generation = 0
    arret = [False] * 10
    while arret != [True]*10:
        l = []
        for e in pop:
            l.append(e[1])
        arg = np.array(l).argsort()
        l.sort()

        generation += 1
        reduire(pop)
        nouvelle_generation(pop,n)
        muter_population(pop, proba)
        
        #vérification de la condition d'arret
        verif = True
        for element in l[0:60]:
            if element != l[0]:
                verif = False
        if verif:
            i = 0
            while arret[i] == True:
                i = i+1
            arret[i] = True
        else:
            arret = [False] * 10
    fin = time.time()
    return pop[arg[0]]# on retourne le meilleur élément

but = 25
taille = 500
proba = 0.15

les_chemins, les_temps = consultation()
but = minute_vers_base_dix(but)

mini = determination_mini(les_temps, but)
maxi = determination_maxi(les_temps, but)

# deteminons les solutions possibles pour atteindre le but
solutions_possibles = []

sol1 = [len(les_chemins)-1-k for k in range(mini+1)]
sol1 = sol1,score_chemin(sol1)
solutions_possibles.append(sol1)

print("Exploration des solutions comprises entre",mini,"et",maxi,".")
for k in range(mini+1, maxi):
    solutions_possibles.append(algo_genetique(taille,k,proba))
    print("Solution de taille",k,"trouvée.")

sol2 = [k for k in range(maxi + 1)]
sol2 = sol2,score_chemin(sol2)
solutions_possibles.append(sol2)

fin = time.time()
print(fin-deb)

#recherche de la meilleure solution:
i_min = 0
for i in range(0,len(solutions_possibles)):
    score = solutions_possibles[i][1]
    if score < solutions_possibles[i_min][1]:
        i_min = i

solutions = []
solutions.append(solutions_possibles[i_min][0])
solutions_possibles.pop(i_min)

selection = []
for i in range(0,len(solutions_possibles)):
    score = solutions_possibles[i][1]
    if score <= but/100:
        solutions.append(solutions_possibles[i][0])

i = rd.randint(0,len(solutions)-1)
commande = "mplayer"
for element in solutions[i]:
    commande += " " + "\"" + str(les_chemins[element]) + "\""
print(commande)
os.system(commande)

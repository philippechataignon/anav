#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import string
import random
from itertools import chain
import networkx as nx
import pickle
import Levenshtein

letters = list(string.ascii_lowercase)

def out(G):
    for n in sorted(G) :
        print(n, G.nodes[n])

def leven(word1,word2):
    """Calcul de la distance de Levenshtein entre 2 mots"""
    #word1 = tri(word1)
    #word2 = tri(word2)
    return Levenshtein.distance(word1, word2)


def tri(s) :
    """ Renvoit le mot trié pour repérage anagramme """
    return "".join(sorted(list(s)))

def cree_dico():
    """constitue dictionnaire des anagrammes depuis dico

    Le dictionnaire renvoyé est de la forme :
        * clé : "mot" constitué des lettres triés
        * valeur : liste des mots anagrammes

        Exemple : 'aimnos': ['aimons', 'amnios', 'maison']
    """
    print('Début lecture')
    with open("gut.txt") as f:
        anag = {}
        for l in f:
            l = l.strip()
            tll = tri(l)
            if tll not in anag:
                anag[tll] = [l]
            else:
                anag[tll].append(l)
    print('Fin lecture')

    with open("gut.pickle", "wb") as f:
        pickle.dump(anag, f)
    return anag

def lis_anag(infile):
    print('Début lecture')
    with open(infile, 'rb') as f:
        anag = pickle.load(f)
    print('Fin lecture')
    return anag

def mots_from(mot):
    """renvoie la liste des mots relié à mot"""
    ch = tri(mot)
    s = set()
    for le in letters :
        s.add(tri(ch + le)) # ajoute
    for i, l in enumerate(ch) :
        base = ch[:i] + ch[i+1:] # enlève lettre
        s.add(base) # enlève lettre
        for le in letters :
            s.add(tri(base + le)) # substitue
    return chain(*(anag.get(ch, []) for ch in s))

def expand(G, curr, cible, atteint=True, explore=False):
    """Etend le graphe depuis curr

    Le node curr passe à l'état explore à True
    On récupère ses voisins et on les ajoute au graphe
    à l'état explore à False

    """
    dist_curr = leven(cible, curr)
    G.add_node(curr, explore=True, dist=dist_curr, atteint=atteint)
    for u in mots_from(curr):
        if u not in G:
            dist = leven(cible, u)
            G.add_node(u, explore=explore, dist=dist, atteint=atteint)
        else :
            G.nodes[u]['atteint'] = atteint
        G.add_edge(curr, u)

def analyse(G, fin, opti):
    """ Analyse du graphe

    Teste si on a une solution
    Définit les noeuds à explorer
    Lance leur exploration
    """

    # Limite recherches
    # On cherche le min des dist + opti

    min_dist = None
    if opti >= 0 :
        min_dist = min([G.nodes[n]['dist'] for n in G if G.nodes[n]['atteint']])
        # les nodes trop lointains sont considérés comme déjà explorés
        for n in G:
            if G.nodes[n]['dist'] > min_dist + opti :
                G.nodes[n]['explore'] = True

    # constition de la liste des nodes non explorés, donc à explorer
    nodes = [n for n in G if not G.nodes[n]['explore']]
    print('Analyse : ', len(nodes), 'nouveaux nodes à explorer - Distance mini :', min_dist)
    for node in nodes :
        expand(G, node, fin)

def cherche(G, debut, fin, max_loop=20, opti=-1):
    """ Boucle principale

    * explore le premier node (debut)
    * puis lance l'analyse des différents niveaux (maximum max_loop)
    * et vérifie si on a trouvé une solution

    """
    # on génère un morceau de graphe par la fin
    expand(G, fin, fin, atteint=False, explore=True)
    nodes = list(G.nodes())
    for n in nodes:
        expand(G, n, fin, atteint=False, explore=True)

    # on génère le début du graphe
    expand(G, debut, fin)
    flag = False
    # puis on élargit progressivement l'analyse et la constitution du graphe
    for level in range(max_loop):
        analyse(G, fin, opti)
        # s'il y a un chemin, on sort
        if nx.has_path(G, debut, fin):
            flag = True
            break
    # indique les différents chemins
    if flag :
        print('100 solutions au hasard :')
        sol = list(nx.all_shortest_paths(G,source=debut,target=fin))
        random.shuffle(sol)
        for i, p in enumerate(sol):
            if i < 100:
                print(p)
        print('Nombre total de solutions :', i+1)

    else:
        print("Pas de chemin trouvé")

if __name__ == '__main__':
    # cree_dico()
    anag = lis_anag("gut.pickle")
    ###cherche(G, 'toiture', 'abricot', opti=2)
    #anag = cree_anag("lmots.txt", "lmots.pickle")
    #cherche(G, 'boite', 'maison', opti=2)
    G = nx.Graph()
    # cherche(G, 'stylo', 'zoulou', opti=2)
    # cherche(G, 'ire', 'hydrotherapique', max_loop=30, opti=4)
    cherche(G, 'vent', 'moulin', opti=2)

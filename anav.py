#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
from itertools import chain
import networkx as nx

letters = list('abcdefghijklmnopqrstuvwxyz')

def leven(word1,word2):
    """Calcul de la distance de Levenshtein entre 2 mots"""
    word1 = tri(word1)
    word2 = tri(word2)
    d = []
    for i in range(len(word1)+1):
        d.append([])
        for j in range(len(word2)+1):
            if i == 0:
                d[i].append(j)
            elif j == 0:
                d[i].append(i)
            else:
                if word1[i-1] == word2[j-1]:
                    cost = 0
                else:
                    cost = 1
                d[i].append(
                    min([
                        d[i-1][j]+1,
                        d[i][j-1]+1,
                        d[i-1][j-1]+cost
                    ])
                )
    return d[-1][-1]

def tri(s) :
    """ Renvoit le mot trié pour repérage anagramme """
    return "".join(sorted(list(s)))

def mots_from(depart):
    """renvoie liste des mots depuis depart"""
    ch = tri(depart)
    s = set()
    for i, l in enumerate(ch) :
        s.add(ch[:i] + ch[i+1:]) # enlève letters
        for le in letters :
            s.add(tri(ch[:i] + le + ch[i+1:])) # substitue
            s.add(tri(ch + le)) # ajoute
    #return chain(anag.get(ch, []) for ch in s)
    out = []
    for ch in s :
        out.extend(anag.get(ch, []))
    return out

def cherche(G, debut, fin, max_loop=20, opti=2):
    """ Boucle principale

    * explore le premier node (debut)
    * puis lance l'analyse des différents niveaux (maximum max_loop)
    * et vérifie si on a trouvé une solution

    """
    expand(G, debut, fin)
    flag = False
    for level in range(max_loop):
        flag = analyse(G, fin, opti)
        # si on a trouvé, on sort
        if flag :
            break
    # indique les différents chemins
    if flag :
        for p in nx.all_shortest_paths(G,source=debut,target=fin):
            print(p)

def analyse(G, fin, opti):
    """ Analyse du graphe

    Teste si on a une solution
    Définit les noeuds à explorer
    Lance leur exploration
    """

    if fin in G :
        print("Fini : ", fin, "trouvé")
        return True

    # Limite recherches
    # On cherche le min des dist + opti

    min_dist = None
    if opti >= 0 :
        min_dist = min([G.node[n]['dist'] for n in G])
        for n in G:
            if G.node[n]['dist'] > min_dist + opti:
                G.node[n]['explore'] = True

    # liste des nodes non explorés
    nodes = list([n for n in G if not G.node[n]['explore']])
    print('Analyse : ', len(nodes), 'nouveaux nodes à explorer - Distance mini :', min_dist)
    for node in nodes :
        expand(G, node, fin)
    return False

def expand(G, curr, fin):
    """Etend le graphe depuis curr

    Le node curr passe à l'état explore à True
    On récupère ses voisins et on les ajoute au graphe
    à l'état explore à False

    """
    dist_curr = leven(fin, curr)
    G.add_node(curr, explore=True, dist=dist_curr)
    for u in mots_from(curr):
        if u not in G:
            dist = leven(fin, u)
            G.add_node(u, explore=False, dist=dist)
        G.add_edge(curr, u)

if __name__ == '__main__':
    print('Début lecture')
    with open("lmots.txt") as f:
        ll = [l.strip() for l in f if len(l)]
    anag = {}
    for l in ll:
        tll = tri(l)
        if tll not in anag:
            anag[tll] = [l]
        else:
            anag[tll].append(l)
    print('Fin lecture')
    #G = nx.Graph()
    #cherche(G, 'casse', 'punir', opti=1)
    #G = nx.Graph()
    #cherche(G, 'bebe', 'vieillard', opti=1)
    G = nx.Graph()
    cherche(G, 'coquelicot', 'colchique', opti=-1)

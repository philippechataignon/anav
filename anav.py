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
    """ Boucle principale """
    expand(G, debut, fin)
    flag = False
    for level in range(max_loop):
        flag = explo(G, fin, opti)
        # si on a trouvé, on sort
        if flag :
            break
    # indique les différents chemins
    if flag :
        for p in nx.all_shortest_paths(G,source=debut,target=fin):
            print(p)

def explo(G, fin, opti):
    if fin in G :
        print("Fini : ", fin, "trouvé")
        return True

    # Limite recherches
    # On cherche le min des dist + opti

    if opti >= 0 :
        min_dist = min([G.node[n]['dist'] for n in G])
        print ('min_dist=', min_dist)
        for n in G:
            if G.node[n]['dist'] > min_dist + opti:
                G.node[n]['explore'] = True

    # liste des nodes non explorés
    nodes = list([n for n in G if not G.node[n]['explore']])
    print('Explo', sorted(nodes))
    for node in nodes :
        expand(G, node, fin)
    return False

def expand(G, curr, fin):
    """Etend le graphe depuis curr"""
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
    G = nx.Graph()
    cherche(G, 'casse', 'punir', opti=0)
    #cherche(G, 'bebe', 'vieillard')
    #cherche(G, 'mot', 'zeste')

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import networkx as nx

def leven(word1,word2):
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
    return "".join(sorted(list(s)))

def mots_from(ll, depart):
    """renvoie liste des mots depuis depart"""
    tri_depart = tri(depart)
    return [l for l in ll if (leven(depart, l) == 1 or tri(l) == tri_depart) and l != depart]

def cherche(G, ll, debut, fin):
    expand(G, ll, debut, fin)
    for level in range(3):
        explo(G, ll, fin)

def explo(G, ll, fin):
    nodes = list(G.nodes())
    print('Explo', nodes)
    for node in nodes :
        if not G.node[node]['explore']:
            expand(G, ll, node, fin)

def expand(G, ll, curr, fin):
    """Etend le graphe depuis curr"""
    G.add_node(curr, explore=True, dist=leven(fin, curr))
    for u in mots_from(ll, curr):
        if u not in G:
            G.add_node(u, explore=False, dist=leven(fin, u))
        G.add_edge(curr, u)

if __name__ == '__main__':
    #import matplotlib.pyplot as plt
    with open("lmots.txt") as f:
        ll = [l.strip() for l in f if len(l) < 6]
    G = nx.Graph()
    cherche(G, ll, 'mot', 'zeste')
    #nx.draw(G)
    #plt.show()

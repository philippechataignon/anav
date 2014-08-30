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
    for level in range(8):
        flag = explo(G, ll, fin)
        if flag :
            break

def explo(G, ll, fin):
    if fin in G :
        print("Fini : ", fin, "trouvé")
        return True

    # Limite recherches
    # On cherche le min des dist

    min_dist = min([G.node[n]['dist'] for n in G])
    for n in G:
        if G.node[n]['dist'] > min_dist + 1 :
            G.node[n]['explore'] = True
    nodes = list([n for n in G if not G.node[n]['explore']])
    print('Explo', sorted(nodes))
    for node in nodes :
        expand(G, ll, node, fin)
    return False

def expand(G, ll, curr, fin):
    """Etend le graphe depuis curr"""
    dist_curr = leven(fin, curr)
    G.add_node(curr, explore=True, dist=dist_curr)
    for u in mots_from(ll, curr):
        if u not in G:
            dist = leven(fin, u)
            G.add_node(u, explore=False, dist=dist)
        G.add_edge(curr, u)

if __name__ == '__main__':
    #import matplotlib.pyplot as plt
    with open("lmots.txt") as f:
        ll = [l.strip() for l in f if len(l) < 7]
    G = nx.Graph()
    cherche(G, ll, 'mot', 'zeste')
    #nx.draw(G)
    #plt.show()

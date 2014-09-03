#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import string
from itertools import chain
#import networkx as nx
import igraph as ig
import cPickle as pickle
import Levenshtein

letters = list(string.ascii_lowercase)

def out(G):
    for n in sorted(G) :
        print(n, G.node[n])


def leven(word1,word2):
    """Calcul de la distance de Levenshtein entre 2 mots"""
    word1 = tri(word1)
    word2 = tri(word2)
    return Levenshtein.distance(word1, word2)

def leven_org(word1,word2):
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

def liste_mots(infile):
    """renvoit la liste des mots (iterateur)"""
    with open(infile) as f:
        for l in f:
            l = l.strip()
            yield l

def cree_anag(infile, outfile):
    """constitue dictionnaire des anagrammes depuis dico

    Le dictionnaire renvoyé est de la forme :
        * clé : "mot" constitué des lettres triés
        * valeur : liste des mots anagrammes

        Exemple : 'aimnos': ['aimons', 'amnios', 'maison']
    """
    print('Début lecture')
    with open(infile) as f:
        anag = {}
        for l in f:
            l = l.strip()
            tll = tri(l)
            if tll not in anag:
                anag[tll] = [l]
            else:
                anag[tll].append(l)
    print('Fin lecture')

    with open(outfile, "w") as f:
        pickle.dump(anag, f)
    return anag

def lis_anag(infile):
    print('Début lecture')
    with open(infile) as f:
        anag = pickle.load(f)
    print('Fin lecture')
    return anag

def mots_from(mot):
    """renvoie la liste des mots relié à mot"""
    ch = tri(mot)
    s = set()
    for i, l in enumerate(ch) :
        s.add(ch[:i] + ch[i+1:]) # enlève letters
        for le in letters :
            s.add(tri(ch[:i] + le + ch[i+1:])) # substitue
            s.add(tri(ch + le)) # ajoute
    return chain(*(anag.get(ch, []) for ch in s))

def expand(G, curr, cible, atteint=True, explore=False):
    """Etend le graphe depuis curr

    Le node curr passe à l'état explore à True
    On récupère ses voisins et on les ajoute au graphe
    à l'état explore à False

    """
    #n = G.vs.find(name=curr)
    print(curr)
    curr["dist"] = leven(curr['name'], cible['name'])
    curr["atteint"] = True
    curr["explore"] = True

    for u in mots_from(curr['name']):
        nu = G.vs.find(name=u)
        if not nu['atteint'] :
            nu['dist'] = leven(cible['name'], u)
        nu['atteint'] = atteint
        G.add_edge(curr, nu)

def analyse(G, fin, opti=-1):
    """ Analyse du graphe

    Teste si on a une solution
    Définit les noeuds à explorer
    Lance leur exploration
    """

    # Limite recherches
    # On cherche le min des dist + opti

    min_dist = None
    if opti >= 0 :
        min_dist = min([G.node[n]['dist'] for n in G if G.node[n]['atteint']])
        # les nodes trop lointains sont considérés comme déjà explorés
        for n in G:
            if G.node[n]['dist'] > min_dist + opti :
                G.node[n]['explore'] = True

    # constition de la liste des nodes non explorés, donc à explorer
    #nodes = [n for n in G if not G.node[n]['explore']]
    new_nodes = G.vs.select(atteint=True).select(explore=False)
    print('Analyse : ', len(new_nodes), 'nouveaux nodes à explorer - Distance mini :', min_dist)
    for node in new_nodes :
        expand(G, node, fin)

def cherche(debut, fin, max_loop=20, opti=-1):
    """ Boucle principale

    * explore le premier node (debut)
    * puis lance l'analyse des différents niveaux (maximum max_loop)
    * et vérifie si on a trouvé une solution

    """
    G = ig.Graph()
    G.add_vertices(400000)
    G.vs['explore'] = False
    G.vs['atteint'] = False
    for i, m in enumerate(liste_mots("lmots.txt")):
        G.vs[i]["name"] = m
    #G.vs['name'] = liste_mots("lmots.txt")
    print(G)
    ## on génère un morceau de graphe par la fin
    #expand(G, fin, fin, atteint=False, explore=True)
    #nodes = list(G.nodes())
    #for n in nodes:
    #    expand(G, n, fin, atteint=False, explore=True)

    ## on génère le début du graphe
    #print(G.vs.find(debut))
    ndebut = G.vs.find(debut)
    nfin   = G.vs.find(fin)
    expand(G, ndebut, nfin)
    flag = False
    # puis on élargit progressivement l'analyse et la constitution du graphe
    for level in range(max_loop):
        analyse(G, nfin, opti)
        # s'il y a un chemin, on sort
        # TODO
        #if nx.has_path(G, debut, fin):
        #    flag = True
        #    break
    # indique les différents chemins
    # TODO
    #if flag :
    #    for p in nx.all_shortest_paths(G,source=debut,target=fin):
    #        print(p)
    #else:
    #    print("Pas de chemin trouvé")

if __name__ == '__main__':
    #cherche(G, 'ire', 'hydrotherapique')
    ###cherche(G, 'toiture', 'abricot', opti=2)
    anag = cree_anag("lmots.txt", "lmots.pickle")
    cherche('boite', 'macon')

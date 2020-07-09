# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import numpy as np
import osmnx as os
import pandas as pa
import networkx as nx
import matplotlib.pyplot as plt

G = os.graph_from_place('Mercy, France', network_type='drive')
#Affiche le Graph
#fig, ax = os.plot_graph(G)

#----------------------------------------------------------------------------------------------------------
#                                               DRONE


#Convertir le MultiGraph en Graph permet de supprimer les aretes redondantes.
g = nx.Graph(G)
def compute_oriented(g):
    # Node de degree impair
    nodes_odd_degree = odd_vertices(g)

    # Combination de toute les nodes de degree impair ensemble
    odd_node_pairs = list(combinations(nodes_odd_degree, 2))
    
    # Pour tout u, v trouver la distance distG(u, v)
    dico_pair_weight = get_shortest_paths_distances(g, odd_node_pairs)

    # Graph complet genere à l'aide du dico des poids
    g_odd_complete = create_complete_graph(dico_pair_weight, flip_weights=True)
    
    # Compute maximum matching
    # Ces lignes sont très bizarre je sais, mais ca marche
    best_matching_odd = dict.fromkeys(nx.algorithms.max_weight_matching(g_odd_complete, True), 0)
    odd_matching = [] # list(pa.unique([tuple(sorted([k, v])) for k, v in best_matching_odd.items()]))
    # Traduire un dico en liste en eliminant les valeurs et en gardant les clés
    for pair in best_matching_odd.items():
        duo = (pair[0][0], pair[0][1])
        odd_matching.append(duo)
    g_aug = add_augmenting_path_to_graph(g, odd_matching)
    return g_aug

    


def solve(is_oriented, num_vertices, edge_list):
    if (is_oriented == False):
        g = nx.Graph(edge_list)
        g = compute_oriented(g)
    else:
        g = nx.DiGraph(edge_list)
        if(not nx.is_eulerian(g)):
            largest = max(nx.strongly_connected_components(G), key=len)
            g = makeStrong(g, largest)
            # Preuve que il est bien strongly Connected
            #print(nx.is_strongly_connected(g))
            g = computegraph(g)
            flowCost, flowDict = nx.network_simplex(g)
            ga = nx.MultiDiGraph(g)
            for key, value in flowDict.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        for i in range (sub_value):
                            ga.add_edge(key, sub_key, weight = g.get_edge_data(key, sub_key)["weight"])
            g = ga
    naive_euler_circuit = list(nx.eulerian_circuit(g))
    print(naive_euler_circuit)
    return naive_euler_circuit
            
#----------------------------------------------------------------------------------------------------------
#                                               DENEIGEUSE
        
def makeStrong(g, largest):
    G = nx.DiGraph(g)
    for e in g.nodes():
        if e not in largest:
            G.remove_node(e)
    return G
    
def computegraph(g):
    temp = 0 # check if correct demand balance
    G = nx.DiGraph()
    for e in g.nodes():
        temp += g.out_degree(e) - g.in_degree(e)
        G.add_node(e, demand = g.out_degree(e) - g.in_degree(e))
    for u, v, w in g.edges(data=True):
        G.add_edge(u,v, weight = round(w["length"]))
    return G
    
          
#----------------------------------------------------------------------------------------------------------
#                                               DRONE
                

def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

# return les nodes de degré impair
def odd_vertices(G):
    nodes_odd_degree = [v for v, d in G.degree() if d % 2 == 1]
    return nodes_odd_degree



def get_shortest_paths_distances(G, pairs):
    distances = dict()
    for pair in pairs:
        distances[pair] = nx.dijkstra_path_length(G, pair[0], pair[1])
    return distances


def create_complete_graph(pair_dico, flip_weights=True):
    g = nx.Graph()
    for k, v in pair_dico.items():
        w = - v if flip_weights else v
        g.add_edge(k[0], k[1] , weight = w)
    return g
   

def add_augmenting_path_to_graph(G, odd_matching):
    augmented_graph = nx.MultiGraph(G.copy())
    for pair in odd_matching:
        augmented_graph.add_edge(pair[0], pair[1],
                    weight =  nx.dijkstra_path_length(G, pair[0], pair[1]))
    return augmented_graph

solve(False, g.order(), g.edges())
#solve(True, G.order(), G.edges(data=True))
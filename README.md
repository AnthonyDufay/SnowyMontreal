# APPERO

La fonction qui expose notre bibliotheque est la fonction solve.
Cette derniere prend trois arguments: 
- un boolean qui indique si le graphe est oriente
- un nombre representant le nombre de noeuds
- une liste de triplets (u, v, w) avec w = poids entre u et v

solve(is_oriented, num_vertices, edge_list)


On considère que si le graphe est non oriet� alors on est dans le cas du parcours du drone, ainsi dans l'autre cas on est dans le cas de la deneigeuse.
Dans tous les cas on peut apparenter le parcours de la déneigeuse et du drone a la resolution du problème du postier chinois.
Un cas simple de ce dernier est la recherche d'un cycle eulérien et le tour est joué.

####### Graphe non oriente ##########

Dans le cas d'un graphe non dirige, la recherche d'une solution se découpe en plusieurs parties:

1)-------------Rendre le Graphe Eulérien------------------------------------------
- trouver tous les noeuds impairs
- réaliser toutes les combinaisons possibes de ces noeuds impairs entre eux
- calculer la distance de ces noeuds
- générer un graph comet a partir du dernier calcul
- trouver un couplage maximum
- ajouter le chemin augmentant au graphe de départ

2)--------------Trouver un Cycle Eulérien------------------------------------------
- trouver un cycle eulérien avec le nouveau graphe

####### Graphe oriente ##########

Pour le cas du graphe orienté, un cas simple est un graphe eu�rien, il suffit de trouver un chemin eulérien.
Dans tous les autres cas, la solution est plus complexe. En effet Pour rendre un graphe orienté eu�rien
il faut que son nombre de edge entrant soit le meme que ceux sortant. 
Pour ce faire on se ramene au problème du min max flow probleme. On considere que les noeuds avec une demande positif (respectivement négatif
sont ceux avec un nombre d'ar�tes sortant supérieur (respectivement inférieurau nombre d'�tes entrant.
A partir du résultat on rajoute lesar�tes manquantes pour former un graphe eulérien et il nous reste plus qua trouver un chemin eulérien.
Notre solution n'est pas adapté avec les graphes qui ne sont pas strongly connected et constitue donc une piste d'amélioration.


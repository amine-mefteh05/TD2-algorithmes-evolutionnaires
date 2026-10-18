from problem import STOCKS, DEMANDES
from utils import calculer_cout

from collections import deque
from copy import deepcopy

def construire_solution():
    """Construit une solution initiale avec le coin nord-ouest."""

    sol = [[0, 0, 0], [0, 0, 0]]

    stocks = STOCKS.copy()
    demandes = DEMANDES.copy()

    i = 0
    m = 0

    while i < len(stocks) and m < len(demandes):
        q = min(stocks[i], demandes[m])

        sol[i][m] = q
        stocks[i] -= q
        demandes[m] -= q

        if stocks[i] == 0:
            i += 1

        if demandes[m] == 0:
            m += 1

    return sol


def generer_voisins(sol):
    """Génère des solutions voisines en modifiant les quantités."""

    voisins = []

    for m1 in range(len(DEMANDES)):
        for m2 in range(len(DEMANDES)):

            if m1 == m2:
                continue

            if sol[0][m1] > 0 and sol[1][m2] > 0:
                voisin = deepcopy(sol)

                # Modifier la répartition entre les deux dépôts
                voisin[0][m1] -= 1
                voisin[0][m2] += 1
                voisin[1][m1] += 1
                voisin[1][m2] -= 1

                voisins.append(voisin)

    return voisins


def recherche_taboue(sol_init, iters=100, taille=5):
    """Recherche une solution de coût minimal."""

    sol = deepcopy(sol_init)
    best = deepcopy(sol_init)

    # Mémoriser les dernières solutions visitées
    tabou = deque(maxlen=taille)

    for _ in range(iters):
        voisins = generer_voisins(sol)

        # Garder les voisins non tabous ou qui améliorent le meilleur coût
        voisins = [
            v for v in voisins
            if v not in tabou
            or calculer_cout(v) < calculer_cout(best)
        ]

        if not voisins:
            break

        # Choisir le voisin ayant le coût le plus faible
        voisin = min(voisins, key=calculer_cout)

        tabou.append(deepcopy(sol))
        sol = voisin

        # Mettre à jour la meilleure solution
        if calculer_cout(sol) < calculer_cout(best):
            best = deepcopy(sol)

    return best

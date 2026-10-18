
from problem import COUTS, STOCKS, DEMANDES


def calculer_cout(sol):
    """Calcule le coût total du transport."""

    cout = 0

    for i in range(len(STOCKS)):
        for j in range(len(DEMANDES)):
            cout += sol[i][j] * COUTS[i][j]

    return cout


def verifier_faisabilite(sol):
    """Vérifie les stocks et les demandes."""

    if len(sol) != len(STOCKS):
        return False

    for ligne in sol:
        if len(ligne) != len(DEMANDES):
            return False

        for q in ligne:
            if not isinstance(q, int) or q < 0:
                return False

    # Vérifier les stocks
    for i in range(len(STOCKS)):
        if sum(sol[i]) != STOCKS[i]:
            return False

    # Vérifier les demandes
    for m in range(len(DEMANDES)):
        q = sum(sol[i][m] for i in range(len(STOCKS)))

        if q != DEMANDES[m]:
            return False

    return True


def afficher_solution(sol, titre):
    """Affiche une solution et son coût."""

    print(f"\n{titre}")

    for i in range(len(sol)):
        print(f"Dépôt D{i + 1} : {sol[i]}")

    print("Coût total :", calculer_cout(sol))

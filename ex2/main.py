
from problem import STOCKS, DEMANDES, COUTS
from tabu_search import construire_solution, recherche_taboue
from utils import calculer_cout, afficher_solution, verifier_faisabilite

def main():
    print("OPTIMISATION DU TRANSPORT PAR RECHERCHE TABOUE")
    print("=" * 48)

    print("\nMatrice des coûts :", COUTS)
    print("Stocks :", STOCKS)
    print("Demandes :", DEMANDES)

    # Vérifier l'équilibre du problème
    if sum(STOCKS) != sum(DEMANDES):
        print("\nLe problème n'est pas équilibré.")
        return

    print("\nLe problème est équilibré.")

    # Construire la solution de départ
    sol_init = construire_solution()
    afficher_solution(sol_init, "Solution initiale")

    # Lancer la recherche taboue
    best = recherche_taboue(sol_init, 100, 5)
    afficher_solution(best, "Meilleure solution trouvée")

    # Vérifier la solution finale
    if verifier_faisabilite(best):
        print("\nLa solution respecte toutes les contraintes.")
    else:
        print("\nLa solution ne respecte pas toutes les contraintes.")

    print("Itérations maximales : 100")
    print("Taille de la liste taboue : 5")


if __name__ == "__main__":
    main()

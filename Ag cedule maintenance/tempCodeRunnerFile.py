
"""TD1 - Cédule de maintenance par algorithme génétique."""

import random
from itertools import product


# ============================================================
# 1. DONNEES DU PROBLEME
# ============================================================

# Puissance des unités 1 à 7 (MW)
CAPACITES = [20, 15, 35, 40, 15, 15, 10]

# Demande des intervalles 1 à 4 (MW)
DEMANDES = [80, 90, 65, 70]

# Puissance totale disponible (MW)
TOTAL = sum(CAPACITES)

# Valeurs autorisées pour chaque gène (4 bits)
GENES = (
    [["1100", "0110", "0011"]] * 2
    + [["1000", "0100", "0010", "0001"]] * 5
)


# ============================================================
# 2. PARAMETRES DE L'ALGORITHME GENETIQUE
# ============================================================

TAILLE_POP = 42
NB_GEN = 20

PC = 0.8
PM = 0.2

GRAINE = 2026


# ============================================================
# 3. CALCUL DES RESERVES ET DE LA FITNESS
# ============================================================

def reserves(chrom):
    """Calcule la réserve de chaque intervalle."""

    res = []

    for t in range(4):
        perdue = sum(
            CAPACITES[u]
            for u in range(7)
            if chrom[u][t] == "1"
        )

        reserve = TOTAL - perdue - DEMANDES[t]
        res.append(reserve)

    return res


def fitness(chrom):
    """Retourne la réserve minimale, ou 0 si elle est négative."""

    return max(0, min(reserves(chrom)))


def texte(chrom):
    """Affiche le chromosome sous forme de chaîne."""

    return " ".join(chrom)


# ============================================================
# 4. GENERATION DE LA POPULATION INITIALE
# ============================================================

def population_initiale():
    """Génère une population aléatoire de 42 chromosomes."""

    return [
        [random.choice(gene) for gene in GENES]
        for _ in range(TAILLE_POP)
    ]


# ============================================================
# 5. SELECTION PAR LOTERIE
# ============================================================

def selection_loterie(pop):
    """Sélectionne un individu selon sa fitness."""

    poids = [fitness(chrom) for chrom in pop]

    # Si toutes les fitness sont nulles
    if sum(poids) == 0:
        return random.choice(pop)

    return random.choices(
        pop,
        weights=poids,
        k=1
    )[0]


# ============================================================
# 6. CROISEMENT A UN POINT
# ============================================================

def croisement(p1, p2):
    """Effectue un croisement entre deux gènes."""

    point = random.randint(1, 6)

    enfant1 = p1[:point] + p2[point:]
    enfant2 = p2[:point] + p1[point:]

    return enfant1, enfant2


# ============================================================
# 7. MUTATION PAR INVERSION
# ============================================================

def mutation_inversion(chrom):
    """Inverse une partie d'un gène si le résultat est autorisé."""

    chrom = chrom[:]

    for i in range(7):

        if random.random() < PM:

            a, b = sorted(random.sample(range(5), 2))

            nouveau = (
                chrom[i][:a]
                + chrom[i][a:b][::-1]
                + chrom[i][b:]
            )

            if nouveau in GENES[i]:
                chrom[i] = nouveau

    return chrom


# ============================================================
# 8. MUTATION PAR REMPLACEMENT
# ============================================================

def mutation_remplacement(chrom):
    """Remplace un gène par une valeur autorisée."""

    chrom = chrom[:]

    for i in range(7):

        if random.random() < PM:

            chrom[i] = random.choice(GENES[i])

    return chrom


# ============================================================
# 9. ALGORITHME GENETIQUE
# ============================================================

def ag(pop, mutation):
    """Exécute l'algorithme génétique."""

    for g in range(1, NB_GEN + 1):

        # Elitisme : conserver le meilleur individu
        elite = max(pop, key=fitness)

        nouvelle = [elite[:]]

        # Génération de la nouvelle population
        while len(nouvelle) < TAILLE_POP:

            # Sélection des parents
            p1 = selection_loterie(pop)
            p2 = selection_loterie(pop)

            # Croisement
            if random.random() < PC:
                e1, e2 = croisement(p1, p2)
            else:
                e1, e2 = p1[:], p2[:]

            # Mutation
            e1 = mutation(e1)
            e2 = mutation(e2)

            nouvelle.extend([e1, e2])

        # Population de taille constante
        pop = nouvelle[:TAILLE_POP]

        # Meilleur individu de la génération
        best = max(pop, key=fitness)

        # Fitness moyenne
        moy = sum(map(fitness, pop)) / TAILLE_POP

        print(
            f"Generation {g:2d} | "
            f"Meilleur = {texte(best)} | "
            f"Fitness = {fitness(best):2d} | "
            f"Moyenne = {moy:5.1f}"
        )

    return max(pop, key=fitness)


# ============================================================
# 10. VERIFICATION EXHAUSTIVE
# ============================================================

def verification_exhaustive():
    """Teste toutes les cédules possibles."""

    toutes = [
        list(chrom)
        for chrom in product(*GENES)
    ]

    valeurs = [
        fitness(chrom)
        for chrom in toutes
    ]

    meilleure = max(valeurs)

    nombre_optimal = valeurs.count(meilleure)

    return len(toutes), meilleure, nombre_optimal


# ============================================================
# 11. PROGRAMME PRINCIPAL
# ============================================================

def main():

    # Exemple de chromosome
    exemple = [
        "0110",
        "0011",
        "0001",
        "1000",
        "0100",
        "0010",
        "1000"
    ]

    print("=" * 60)
    print("EXEMPLE DE CHROMOSOME")
    print("=" * 60)

    print("Chromosome :", texte(exemple))
    print("Reserves   :", reserves(exemple))
    print("Fitness    :", fitness(exemple))

    # Initialisation aléatoire reproductible
    random.seed(GRAINE)

    depart = population_initiale()

    resultats = {}

    # Comparaison des deux méthodes de mutation
    mutations = [
        ("Inversion", mutation_inversion),
        ("Remplacement", mutation_remplacement)
    ]

    for nom, mutation in mutations:

        print()
        print("=" * 60)
        print("MUTATION PAR", nom.upper())
        print("=" * 60)

        resultats[nom] = ag(
            [chrom[:] for chrom in depart],
            mutation
        )

    # Résultats finaux
    print()
    print("=" * 60)
    print("RESULTATS FINAUX")
    print("=" * 60)

    for nom, chrom in resultats.items():

        print()
        print("Mutation :", nom)
        print("Chromosome :", texte(chrom))
        print("Reserves :", reserves(chrom))
        print("Fitness :", fitness(chrom))

    # Vérification exhaustive
    n, best, nb = verification_exhaustive()

    print()
    print("=" * 60)
    print("VERIFICATION EXHAUSTIVE")
    print("=" * 60)

    print("Nombre de cédules testées :", n)
    print("Fitness maximale :", best)
    print("Nombre de solutions optimales :", nb)


# ============================================================
# EXECUTION
# ============================================================

if __name__ == "__main__":
    main()

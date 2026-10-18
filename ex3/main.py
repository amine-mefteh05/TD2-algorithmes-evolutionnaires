
from problem import VILLES, INITIAL
from utils import cout

from tabu_search import tabou
from recuit_simule import recuit


print("Circuit initial :", INITIAL + [INITIAL[0]])
print("Coût initial :", cout(INITIAL, VILLES))

s, d = tabou(INITIAL, VILLES, 5, 3)
print("\nRecherche taboue :", s + [s[0]], "| Coût :", d)

s, d = recuit(INITIAL, VILLES, 5)
print("Recuit simulé :", s + [s[0]], "| Coût :", d)

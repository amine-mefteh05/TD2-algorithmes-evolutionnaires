
from math import exp, log
from random import choice, random
from problem import VILLES, INITIAL
from utils import cout
from tabu_search import voisins


def recuit(initial, villes, iters):
    s = initial[:]
    meilleur = s[:]
    d = cout(s, villes)
    d_min = d

    hausses = [
        cout(v, villes) - d
        for v in voisins(s, villes)
        if cout(v, villes) > d
    ]

    t = -(sum(hausses) / len(hausses)) / log(0.8) if hausses else 1
    alpha = 0.8

    for _ in range(iters):
        candidats = voisins(s, villes)

        if not candidats:
            break

        v = choice(candidats)
        delta = cout(v, villes) - d

        if delta <= 0 or random() < exp(-delta / t):
            s = v
            d = cout(s, villes)

        if d < d_min:
            meilleur = s[:]
            d_min = d

        t *= alpha

    return meilleur, d_min


def main():
    s, d = recuit(INITIAL, VILLES, 5)
    print("Circuit :", s + [s[0]])
    print("Coût :", d)


if __name__ == "__main__":
    main()

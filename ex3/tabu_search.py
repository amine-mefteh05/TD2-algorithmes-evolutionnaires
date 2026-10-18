
from collections import deque
from problem import VILLES, INITIAL
from utils import cout, est_valide


def voisins(s, villes):
    res = []

    for i in range(1, len(s) - 1):
        for j in range(i + 1, len(s)):
            v = s[:]
            v[i], v[j] = v[j], v[i]

            if est_valide(v, villes):
                res.append(v)

    return res


def tabou(initial, villes, iters, taille):
    s = initial[:]
    meilleur = s[:]
    d = cout(s, villes)
    d_min = d
    tab = deque(maxlen=taille)

    for _ in range(iters):
        candidats = [
            v for v in voisins(s, villes)
            if v not in tab or cout(v, villes) < d_min
        ]

        if not candidats:
            break

        v = min(candidats, key=lambda x: cout(x, villes))
        tab.append(s[:])
        s = v
        d = cout(s, villes)

        if d < d_min:
            meilleur = s[:]
            d_min = d

    return meilleur, d_min


def main():
    s, d = tabou(INITIAL, VILLES, 5, 3)
    print("Circuit :", s + [s[0]])
    print("Coût :", d)


if __name__ == "__main__":
    main()

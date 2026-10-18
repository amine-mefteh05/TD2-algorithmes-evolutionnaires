
def est_valide(s, villes):
    for i in range(len(s)):
        a = s[i] - 1
        b = s[(i + 1) % len(s)] - 1

        if villes[a][b] == -1:
            return False

    return True


def cout(s, villes):
    if not est_valide(s, villes):
        return float("inf")

    total = 0
    for i in range(len(s)):
        a = s[i] - 1
        b = s[(i + 1) % len(s)] - 1
        total += villes[a][b]

    return total

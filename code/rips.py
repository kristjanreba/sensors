import math


def BronKerbosch(R, P, X, EG):
    klike = set()

    if len(P) == 0 and len(X) == 0:
        pomozna = {tuple(sorted([R[j] for j in range(len(R)) if (i & (2 ** j))])) for i in range(1, 2 ** (len(R)))}
        klike = klike.union(pomozna)

    for v in P:
        sosedi = set()
        for e in EG:
            if e[0] == v:
                sosedi.add(e[1])
            elif e[1] == v:
                sosedi.add(e[0])

        klike = klike.union(BronKerbosch(R + [v], P.intersection(sosedi), X.intersection(sosedi), EG))
        P = P.difference({v})
        X = X.union({v})

    return klike


def cliques(VG, EG):
    klikeM = BronKerbosch([], set(VG), set(), EG)
    klikeD = dict()
    for x in klikeM:
        l = len(x)
        if l in klikeD:
            klikeD[l].append(x)
            klikeD[l] = sorted(klikeD[l])
        else:
            klikeD[l] = [x]

    klike = dict(sorted(klikeD.items()))
    return klike


def VR(S, epsilon):
    EG = []
    VG = []
    for i in range(len(S)):
        VG.append(i)
        for j in range(i + 1, len(S)):
            d = math.sqrt((S[j][0] - S[i][0]) ** 2 + (S[j][1] - S[i][1]) ** 2 + (S[j][2] - S[i][2]) ** 2)
            if d <= epsilon:
                EG.append(tuple(sorted((i, j))))

    ripsP = cliques(VG, EG)
    rips = dict()
    for k, v in ripsP.items():
        rips[k - 1] = ripsP[k]
    return rips

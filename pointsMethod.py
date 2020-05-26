from task import Task
import numpy as np
from itertools import combinations
from accessify import private

Eps = 0.00001

def findAll(Zd: Task):
    NList = combinations(list(range(len(Zd.A[0]))), len(Zd.A))

    for N in NList:
        Ak = np.array([Zd.A[:, i] for i in N]).T

        if np.abs(np.linalg.det(Ak)) > Eps:
            xNk = np.matmul(np.linalg.inv(Ak), Zd.B)
            if np.min(xNk) < 0:
                continue

            xN = np.zeros(len(Zd.A[0]))

            for i in range(len(N)):
                xN[N[i]] = xNk[i]

            yield xN


def methodMain(Zd: Task):
    all = list(findAll(Zd))

    if not all:
        return np.zeros(len(Zd.A[0]))

    min = all[0]

    for i in all[1:]:
        if np.dot(i, Zd.C) < np.dot(min, Zd.C):
            min = i

    return min

from task import Task
import numpy as np
from itertools import combinations


def splitXkN(xkN):
    """Для получения N+, N0, X+, X0"""
    NkPlus = np.array(list(filter(lambda i: xkN[i] > 0, range(len(xkN)))))
    Nk0 = np.array(list(filter(lambda i: xkN[i] == 0, range(len(xkN)))))

    xkNPlus = np.array(list(filter(lambda i: i > 0, xkN)))
    xkN0 = np.array(list(filter(lambda i: i == 0, xkN)))

    return xkNPlus, NkPlus, xkN0, Nk0


def basisSolve(a: Task):
    """Метод искусственного базиса, насколько я понимаю именно такая реализация и нужна"""
    A, B = a.A, a.B
    EMM = np.eye(len(B))

    ADop = np.concatenate((A, EMM), axis=1)
    cDop = np.concatenate((np.zeros(len(A[0])), np.ones(len(B))))

    tmp = Task(ADop, B, cDop)
    xStart = np.concatenate(((np.zeros(len(a.C)), B)))

    xk, Nk, end = Simplex(tmp, xStart)
    
    yM = xk[len(A[0]):]
    if not end or np.max(yM) > 0:
        return np.array([np.inf for _ in range(len(A))]), np.array([]), np.array([]), False
    
    x0N = xk[:len(A[0])]
    _, NkPlus,_,_ = splitXkN(x0N)
    
    if len(NkPlus) == len(B):
        return x0N, Nk, NkPlus, True
    print("Need another vect")


def solveDoubleProblem(a: Task):
    A, B = a.A, a.B
    EMM = np.eye(len(B))

    ADop = np.concatenate((A, EMM), axis=1)
    cDop = np.concatenate((np.zeros(len(A[0])), np.ones(len(B))))

    tmp = Task(ADop, B, cDop)
    xStart = np.concatenate(((np.zeros(len(a.C)), B)))

    xk, Nk, end = Simplex(tmp, xStart)

    yM = xk[len(A[0]):]
    if not end or np.max(yM) > 0:
        return np.array([np.inf for _ in range(len(A))]), np.array([]), np.array([]), False

    x0N = xk[:len(A[0])]
    _, NkPlus, _, _ = splitXkN(x0N)

    if len(NkPlus) == len(B):
        return x0N, Nk, NkPlus, True
    print("Need another vect")

def Simplex(a:Task, xk0, maxIters = 50):
    """Собственно мы тут вызываем симплекс метод, нужно, чтобы можно было выбрать базис"""
    xkN, Nk = xk0, np.array([])

    for _ in range(maxIters):
        xkN, Nk, end = simplexK(a, xkN)
        if end:
            break

    if len(Nk) == 0 or np.max(xkN) == np.inf:
        return xkN, Nk, False
    else:
        return xkN, Nk, True


def startVect(a:Task):
    """Классический метод выбора начального базиса, вроде нам не нужен пока что"""
    NList = combinations(list(range(len(a.A[0]))), len(a.B))

    for Nk in NList:
        Ak = np.array([cf.A[:, i] for i in Nk]).T

        if np.linalg.det(Ak) != 0:
            xNk = np.matmul(np.linalg.inv(Ak), a.B)
            xN = np.zeros(len(A[0]))

            for i in range(len(Nk)):
                xN[Nk[i]] = xNk[i]
            return xN

    return np.zeros(len(A[0]))


def simplexK(a:Task, xkN):
    """Симлекс метод, данная вариация описана в учебнике"""
    A, C = a.A, a.C
    _, NPlus, _, N0 = splitXkN(xkN)

    check = len(a.B) - len(NPlus) if len(a.B) - len(NPlus) != 0 else 1
    NList = combinations(list(range(len(N0))), len(a.B) - len(NPlus))

    for Nk in NList:
        Nk = list(Nk)
        for i in NPlus:
            Nk.append(i)
        Ak = np.array([A[:, i] for i in Nk]).T

        _, NkPlus, _, Nk0 = splitXkN(xkN)
        Lk = np.array(list(filter(lambda idx: idx not in Nk, Nk0))).astype(int)

        if np.linalg.det(Ak) == 0:
            continue

        AInvk = np.linalg.inv(Ak)

        CNk = np.array([C[i] for i in Nk])
        ykM = np.matmul(AInvk.T, CNk)
        dkN = C - np.matmul(A.T, ykM)
        dkLk = np.array([dkN[int(i)] for i in Lk])

        if np.min(dkLk) >= 0:
            return xkN, Nk, True

        jk = Lk[list(filter(lambda j: dkLk[j] < 0, range(len(Lk))))[0]]
        ukNk = np.matmul(AInvk, A[:, jk])

        if np.max(ukNk) <= 0:
            return np.array(list(np.inf for _ in range(len(A[0])))), Nk, True

        _, NkPlus, _, Nk0 = splitXkN(xkN)

        if len(NkPlus) == len(Nk) \
                or max([ukNk[i] for i in filter(lambda j: Nk[j] not in NkPlus, range(len(Nk)))]) < 0:

            ukN = [ukNk[list(Nk).index(i)] if i in Nk else 0 for i in range(len(A[0]))]
            ukN[jk] = -1

            thetaK = min([xkN[i] / ukN[i] for i in filter(lambda j: ukN[j] > 0, Nk)])

            return xkN - np.multiply(thetaK, ukN), Nk, False

        return xkN, np.array([]), True
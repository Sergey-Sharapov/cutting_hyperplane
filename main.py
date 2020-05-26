import numpy
from numpy import linalg

from InpOut import *
from double import Double
from task import Task
import simplex

eps = 0.01


def phi1(x: list):
    return 3 * x[0] ^ 2 + x[1] ^ 2 - 1


def phi2(x: list):
    return x[0] ^ 2 + (x[1] - 1 / 2) ^ 2 - 1 / 2


def phi(x):
    return max(phi1(x), phi2(x))


def grad_phi1(x):
    return [6 * x[0], 2 * x[1]]


def grad_phi2(x):
    return [2 * x[0], 2 * x[1] - 1]


def gen_sub_grad(x):
    if phi1(x) >= phi2(x):
        return grad_phi1(x)
    else:
        return grad_phi2(x)


Input = Read("input.txt")
Output = Write("output.txt")

liner_problem = Task(Input.A, Input.B, Input.C)
double_liner_problem = Double(liner_problem)

resY, Nk, resN, _ = simplex.solveDoubleProblem(double_liner_problem)
resX = double_liner_problem.reconstSol(double_liner_problem, Nk)

k = 0
while True:
    if phi1(resX) <= 0 & phi2(resX) <= 0:
        print("Solved: " + resX)
    else:
        if k >= 1 & linalg.norm([resX[i] - oldX[i] for i in range(len(resX))]) < eps:
            print("Solved: " + resX)
        else:
            sub_grad = gen_sub_grad(resX)
            b_new = - phi(resX) + numpy.dot(sub_grad, resX)
            #
            k = k + 1

import numpy
from numpy import linalg
from scipy.optimize import linprog

import double
from InpOut import *
from double import Double
from task import Task
import simplex

eps = 0.01

def phi1(x: list):
    return 3 * x[0] ^ 2 + x[1] ^ 2 - 1

def phi2(x: list):
    return x[0] ^ 2 + (x[1] - 1 / 2) ^ 2 - 1 / 2

def phi3(x: list):
    return 3 * x[0] ^ 2 + x[1] ^ 2 - 1 - x[2]

def phi(x):
    return max(phi1(x), phi2(x), phi3(x))

def grad_phi1(x):
    return [6 * x[0], 2 * x[1], 0]

def grad_phi2(x):
    return [2 * x[0], 2 * x[1] - 1, 0]

def grad_phi3(x):
    return [6 * x[0], 2 * x[1], -1]

def gen_sub_grad(x):
    if phi1(x) >= phi2(x):
        if phi1(x) >= phi3(x):
            return grad_phi1(x)
        else:
            return grad_phi3(x)
    else:
        if phi3(x) >= phi2(x):
            return grad_phi3(x)
        else:
            return grad_phi2(x)

Input = Read("input.txt")
Output = Write("output.txt")

liner_problem = Task(Input.A, Input.B, Input.C)
double_liner_problem = Double(liner_problem)

lp_tmp = liner_problem
dlp_tmp = double_liner_problem

#resY, Nk, resN, _ = simplex.solveDoubleProblem(double_liner_problem)
#resX = double_liner_problem.reconstSol(double_liner_problem, Nk)

resultY = linprog(dlp_tmp.C, A_eq=dlp_tmp.A, b_eq=dlp_tmp.B)
n_k = []
for i in range(len(resultY.x)):
    if resultY.x[i] != 0:
        n_k.append(i)

#resX = Double.reconstSol(dlp_tmp, n_k)
resX = linprog(lp_tmp.C, A_ub=lp_tmp.A, b_ub=lp_tmp.B, bounds=(None, None))

oldX = []
while True:
    if phi1(resX) <= 0 & phi2(resX) <= 0:
        print("Solved: " + resX)
        break
    else:
        sub_grad = gen_sub_grad(resX)
        b_new = - phi(resX) + numpy.dot(sub_grad, resX)
        lp_tmp.A.add(sub_grad)
        lp_tmp.B.add(b_new)

        oldX = resX
        #resY, Nk, resN, _ = simplex.solveDoubleProblem(lp_tmp)
        #resX = double_liner_problem.reconstSol(dlp_tmp, Nk)

        resultY = linprog(dlp_tmp.C, a_eq=dlp_tmp.A, b_eq=dlp_tmp.B)
        n_k = []
        for i in range(len(resultY.x)):
            if resultY.x != 0:
                n_k.append(i)
        resX = Double.reconstSol(dlp_tmp, n_k)

        if linalg.norm([resX[i] - oldX[i] for i in range(len(resX))]) < eps:
            print("Solved: " + resX)
            break


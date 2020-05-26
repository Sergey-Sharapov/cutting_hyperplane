from task import Task
import numpy as np
from  double import Double
from pointsMethod import methodMain
from simplex import *
#1, проверяем работу построеня двойственной задачи из канонической
#A = np.array([[-1, 3, -5], [2, -1, 4], [3, 1, 1]])
#B = np.array([12, 24, 18])
#C = np.array([2, 1, 3])
#
#Answer not exist
#a = Task(A, B, C)
#a.print()
#ad = Double(a)
#ad.print()
#
#
A = np.array([[0, -1, 1, 1, 0], [-5, 1, 1, 0, 0], [-8, 1, 2, 0, -1]])
B = np.array([1, 2, 3])
C = np.array([3, -2, -4, 0, 0])
#Answer:[1, 3, 4, 0, 0]
#AnswerDouble:[0, 0, 0, 13, 24]
a = Task(A, B, C)

ad = Double(a)

Sol = methodMain(a)
print(a.otherRes(Sol))
Solad = methodMain(ad)

print(ad.otherRes(Solad))
#resX, resN, _ = basisSolve(a)
#print(resX, resN)
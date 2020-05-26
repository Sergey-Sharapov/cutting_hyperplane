from task import Task
import numpy as np
from  double import Double
from pointsMethod import methodMain
from simplex import *
from InpOut import *


Input = Read("input.txt")
Output = Write("output.txt")
#задача
a = Task(Input.A, Input.B, Input.C)
#двойственная задача
ad = Double(a)
#метод крайних точек
Sol = methodMain(a)

Output.write(Sol, "Answer with points meth")

#а теперь искусственным базисом решим
resX, Nk, resN, _ = basisSolve(a)
Output.write(resX, "Simplex ans")
Output.write(resN, "N for simplex ans")

#восстановление решения
y = ad.reconstSol(a, Nk)
print(y)
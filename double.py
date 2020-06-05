#Строим двойственную задачу ЛП
#считаем, что задача уже сведена к каноническому виду, потому что см.п.1 на гите
from task import Task
from accessify import private
import numpy as np

class Double(Task):
    @private
    def toCanoinan(self):
        Atmp = list(list())
        Ctmp = list()
        len0A = len(self.A)

        for i in range(len(self.A)):
            Atmp.append(list())
            for j in range(len(self.A[i])):
                Atmp[i].append(self.A[i][j])
                Atmp[i].append(-self.A[i][j])

        for i in range(len(self.C)):
            Ctmp.append(self.C[i])
            Ctmp.append(-self.C[i])

        self.A = Atmp
        self.C = Ctmp

        for i in range(len0A):
            for j in range(i):
                self.A[i].append(0)

            self.A[i].append(1)

            for j in range(len0A - i - 1):
                self.A[i].append(0)

            self.C.append(0);

        self.A = np.array(self.A)
        self.C = np.array(self.C)

        for i in range(len(self.B)):
            if self.B[i] < 0:
                self.A[i] = -1 * self.A[i]
                self.B[i] = -1 * self.B[i]

    def __init__(self, Task):
        self.A = np.copy(np.transpose(Task.A))
        self.C = np.copy(-Task.B)
        self.B = np.copy(Task.C)
        #self.toCanoinan()

    @staticmethod
    def reconstSol(task, Nk):
        #print(Nk)
        c = np.array(task.C)
        c_Nk = []
        A_tmp = []
        print(task.A)

        for nk_i in range(len(Nk)):
            A_tmp.append([])
            c_Nk.append(c[Nk[nk_i]])
            for i in range(len(task.A)):
                A_tmp[nk_i].append(task.A[i][Nk[nk_i]])
        print(A_tmp)

        A_tmp = np.transpose(np.array(A_tmp))
        A_inv = np.linalg.inv(A_tmp)
        c_Nk = np.array(c_Nk)
        x = c_Nk.dot(A_inv)
        return x

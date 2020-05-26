#мы подразумеваем, что у нас каноническая задача
import numpy as np


class Task:
    def __init__(self, A, B, C):
        self.C = C
        self.A = A
        self.B = B
        
        ''''
        for i in range(len(B)):
            if self.B[i] < 0:
                self.A[i] = -1 * self.A[i]
                self.B[i] = -1 * self.B[i]
                
        '''''

    def print(self):
        for i in range(len(self.A)):
            for j in range(len(self.A[i]) - 1):
                print(str(self.A[i][j]) + '*X' + str(j) + ' + ', end="")

            print(str(self.A[i][j + 1]) + '*X' + str(j + 1) + ' = ' + str(self.B[i]))

        for i in range(len(self.C) - 1):
            print(str(self.C[i]) + '*X' + str(i) + ' + ', end="")
        print(str(self.C[i + 1]) +'*X' + str(i + 1) + '->min')

        for i in range(len(self.C)):
            print('X' + str(i) + ' >= 0', end=" ")
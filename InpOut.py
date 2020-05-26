import numpy as np


class Read:
    """Для считывания, с обработкой для общего случая, считыванием каноническую матрицу"""

    def __init__(self, fileName):
        self.file = open(fileName, 'r')
        self.A = list([])
        self.B = list()
        self.C = list()
        
        self.Read()

    def Read(self):
        i = 0
        for line in self.file:
            str = line.split()
            self.A.append(list())

            for numb in str[:len(str) - 1]:
                self.A[i].append(int(numb))
            self.B.append(str[len(str) - 1])

            i += 1

        for j in self.A[i - 1][:len(self.A[i - 1])]:
            self.C.append(j)

        self.C = np.array(self.C)

        if self.B[len(self.B) - 1] == 'max':
            self.C *= -1

        tmpB = list()

        for j in self.B[:len(self.B) - 1]:
            tmpB.append(int(j))

        self.B = np.array(tmpB)
        self.A = np.array(self.A[:i - 1])

        self.file.close()

class Write:
    def __init__(self, fileName):
        self.file = open(fileName, 'w')

    def write(self, data, comment):
        for i in data:
            self.file.write(str(i) + " ")
        
        self.file.write('#   ' + comment)
        self.file.write('\n')
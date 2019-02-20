from mytools2 import hs, genMatrix, P, coff, mymul, mydiv, mysub, myadd, myGetRandomElement
import numpy as np

class Worker:
    def __init__(self, id, A1, B1, d, S):
        self.id = id
        self.d = d
        self.S = S
        self.A1 = A1
        self.B1 = B1
        self.I_star = []
        self.I_ab = []
        self.I = []

    def IntEnc(self, I):
        self.I = []
        self.I_ab = []
        self.I_star = []

        for w in I:
            templist = []
            for i in range(0, self.d + 1):
                templist.append((hs(w) ** i)%P)
            self.I.append(templist)
            I_a = genMatrix((self.d + 1, 1))
            I_b = genMatrix((self.d + 1, 1))
            for i in range(0, self.d + 1):
                if self.S[i] == 0:
                    I_a[i, 0] = templist[i]
                    I_b[i, 0] = templist[i]
                else:
                    I_a[i, 0] = myGetRandomElement()
                    #I_a[i] = random.uniform(*sorted([0, templist[i]]))
                    I_b[i, 0] = mysub(templist[i], I_a[i, 0])
            self.I_ab.append([I_a, I_b])
            tempA1 = self.A1.Copy()
            tempA1.Transpose()
            tempB1 = self.B1.Copy()
            tempB1.Transpose()
            self.I_star.append([tempA1*I_a, tempB1*I_b])


class Broker:
    def __init__(self):
        self.rk = dict()

    def addRK(self, id, rk):
        self.rk[id] = rk

    def IntTran(self, id, I_star):
        A2, B2 = self.rk[id]
        tempA2 = A2.Copy()
        tempA2.Transpose()
        tempB2 = B2.Copy()
        tempB2.Transpose()
        self.I_tilde = [[tempA2 * item1, tempB2 * item2] for item1, item2 in I_star]

    def TdTran(self, id, T):
        A2, B2 = self.rk[id]
        self.T_tilde =  [A2.Inverse() * T[0], B2.Inverse() * T[1]]

    def Match(self):
        for I_j in self.I_tilde:
            tempCopy1 = self.T_tilde[0].Copy()
            tempCopy1.Transpose()

            tempCopy2 = self.T_tilde[1].Copy()
            tempCopy2.Transpose()
            temp = tempCopy1*I_j[0] + tempCopy2*I_j[1]
            # print(temp)
            if temp[0,0] == 0:
                return 1
        return 0


class Requester:
    def __init__(self, id, A1, B1, d, S):
        self.d = d
        self.S = S
        self.id = id
        self.A1 = A1
        self.B1 = B1
        self.T = None
        self.Q_vector = None
        self.Q_ab = []

    def TdGen(self, Q):
        l = self.d-len(Q)
        Q = Q + ['eeee']*l
        H_Q_list = [mysub(0, hs(i)) for i in Q]
        Q_vector = [coff(H_Q_list, i) for i in range(0, self.d+1)]
        self.Q_vector = Q_vector
        Q_vector_a = genMatrix((self.d + 1, 1))
        Q_vector_b = genMatrix((self.d + 1, 1))
        for k,i in enumerate(self.S):
            if i == 0:
                Q_vector_a[k, 0] = myGetRandomElement()
                #Q_vector_a[k] = random.uniform(*sorted([0, Q_vector[k]]))
                Q_vector_b[k, 0] = mysub(Q_vector[k], Q_vector_a[k, 0])
            else:
                Q_vector_a[k, 0] = Q_vector[k]
                Q_vector_b[k, 0] = Q_vector[k]
        self.T = [self.A1.Inverse()*Q_vector_a, self.B1.Inverse()*Q_vector_b]
        self.Q_ab = [Q_vector_a, Q_vector_b]

class KMS:
    def __init__(self, d):
        # Setup
        self.d = d
        self.S = np.random.randint(0, 2, size=d+1)
        self.M1 = genMatrix((d + 1, d + 1))
        self.M2 = genMatrix((d + 1, d + 1))

    def KeyGen(self, broker, id, worker=True):
        A1 = genMatrix((self.d + 1, self.d + 1))
        B1 = genMatrix((self.d + 1, self.d + 1))
        A2 = A1.Inverse() * self.M1
        B2 = B1.Inverse() * self.M2
        broker.addRK(id, [A2, B2])

        if worker:
            return Worker(id, A1, B1, self.d, self.S)
        else:
            return Requester(id, A1, B1, self.d, self.S)


if __name__ == '__main__':
    kms = KMS(6)
    print(kms.S)

import numpy as np
import matplotlib.pyplot as plt
import random


def zero():
    z = []
    for i in range(0, 273):
        b = 0
        z.append(b)
    return z


def H_Z_t(H, Z):
    h_z = []
    for i in range(0, 273):
        m = 0
        for j in range(0, 546):
            m = np.add(np.multiply(H[i][j], Z[0][j]), m)
            if m % 2 == 0:
                m = 0
            else:
                m = 1
        h_z.append(m)
    return h_z


def paritycheck():
    matrix_1 = np.zeros((273, 546), dtype=np.int64)
    matrix__0 = np.identity(91, dtype=np.int64)
    matrix__1 = np.roll(matrix__0, -1, axis=0)
    matrix__6 = np.roll(matrix__0, -6, axis=0)
    matrix__28 = np.roll(matrix__0, -28, axis=0)
    matrix__40 = np.roll(matrix__0, -40, axis=0)
    matrix__48 = np.roll(matrix__0, -48, axis=0)
    matrix__10 = np.roll(matrix__0, -10, axis=0)
    matrix__60 = np.roll(matrix__0, -60, axis=0)
    matrix__7 = np.roll(matrix__0, -7, axis=0)
    matrix__36 = np.roll(matrix__0, -36, axis=0)
    matrix__25 = np.roll(matrix__0, -25, axis=0)
    #
    matrix_1[0:91, 0:91] = matrix__0
    matrix_1[0:91, 91:182] = matrix__0
    matrix_1[0:91, 182:273] = matrix__0
    matrix_1[0:91, 273:364] = matrix__0
    matrix_1[0:91, 364:455] = matrix__0
    matrix_1[0:91, 455:546] = matrix__0
    matrix_1[91:182, 0:91] = matrix__0
    matrix_1[182:273, 0:91] = matrix__0
    matrix_1[91:182, 91:182] = matrix__1
    matrix_1[91:182, 182:273] = matrix__6
    matrix_1[91:182, 273:364] = matrix__28
    matrix_1[91:182, 364:455] = matrix__40
    matrix_1[91:182, 455:546] = matrix__48
    matrix_1[182:273, 91:182] = matrix__10
    matrix_1[182:273, 182:273] = matrix__60
    matrix_1[182:273, 273:364] = matrix__7
    matrix_1[182:273, 364:455] = matrix__36
    matrix_1[182:273, 455:546] = matrix__25
    H = matrix_1
    return H


def sumproduct(vector_r, H):
    print("sumproduct")
    r = vector_r

    # parity check matrix

    print(H)

    # sum_product Algorithm
    B = []
    for i in range(0, 273):
        b = []
        B.append(b)
        for j in range(0, 546):
            if H[i][j] == 1:
                b.append(j)
                print(f"B={B}")

    A = []
    for j in range(0, 546):
        a = []
        A.append(a)
        for i in range(0, 273):
            if H[i][j] == 1:
                a.append(i)
                print(f"A={A}")
    M = np.zeros((273, 546))
    # r = np.array([-0.5,2.5,-4.0,5.0,-3.5,2.5])

    E = np.zeros((273, 546), dtype=float)
    L = np.zeros((1, 546), dtype=float)
    Z = np.zeros((1, 546), dtype=int)
    for i in range(0, 546):  # Initialization
        for j in range(0, 273):
            M[j][i] = r[0][i]

    # print(f"M={M}")
    for I in range(0, 50):
        for j in range(0, 273):  # step1:Check messages
            for i in B[j]:
                n = 1
                for t in B[j]:
                    if t != i:
                        n = np.multiply(np.tanh(M[j][t] / 2), n)
                E[j][i] = np.log((1 + n) / (1 - n))
                # print(f"E={E}")
        for i in range(0, 546):  # Test
            m = 0
            for j in A[i]:
                m = np.add(E[j][i], m)
            L[0][i] = m + r[0][i]
            if L[0][i] <= 0:
                Z[0][i] = 1
            else:
                Z[0][i] = 0
        # print(f"L={L}")
        # print(f"Z={Z}")
        # print(f"H={H}")

        y = H_Z_t(H, Z)

        # print(f"HZ.T={y}")

        s = zero()

        if (I == 50) or (y == s):
            return Z
        else:
            for i in range(0, 546):  # Step2:Bit messages
                for j in A[i]:
                    m = 0
                    for t in A[i]:
                        if t != j:
                            m = E[t][i] + m
                    M[j][i] = m + r[0][i]
            I += 1
    #     print(f"I={I}")
    #     print(f"M={M}")
    return Z


def simulation(snr):
    print("simulation")
    SNR = snr
    m = 273
    n = 546
    K = n - m
    R = K / n
    N_0 = 1 / (R * (10 ** (SNR / 10)))
    variance = N_0 / 2
    E_b = 0  # bit errors
    E_f = 0  # frame errors
    x = 0  # x is the number of block y
    BPSK_0 = np.ones((1, 546))
    r = np.zeros((1, 546), dtype=float)
    while E_f < 30:
        z = np.sqrt(variance) * np.random.normal(size=546)  # print(np.random.normal(size=5))
        y = BPSK_0 + z
        for i in range(0, 546):
            r[0][i] = (4 / N_0) * y[0][i]
        H = paritycheck()
        C = sumproduct(r, H)
        x = x + 1
        print(f"x={x}")
        e = 0
        for i in C[0]:
            e = np.add(i, e)
        print(f"e={e}")
        if e > 0:
            E_f = E_f + 1
            E_b = E_b + e
        else:
            print("c is not error")

    BER = E_b / (546 * x)
    FER = 30 / x
    BER_FER = [BER, FER]
    print(f"[BER,FER]={BER_FER}")
    return BER_FER


def RUN(i, dtype=int):
    print("run")
    element_1 = []
    element_2 = []
    for SNR in range(0, i):
        X = simulation(SNR)
        x = X[0]
        element_1.append(x)
        y = X[1]
        element_2.append(y)
    plt.plot(range(0, i), element_1, color=('red'))
    plt.plot(range(0, i), element_2, color=('blue'))
    plt.title("Erroe Rates of a QC-LDPC Code")
    plt.xlabel('SNR=E_b/N_0(db)')
    plt.ylabel('BER/FER')
    plt.legend(['BER', 'FER'])
    plt.show()
    return print('jafar ghodrati')


RUN(1)
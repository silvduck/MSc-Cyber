# Silvia Sanvicente, maig 2022, UOC - MUCiberSec - Advanced Cryptography

import numpy as np
import math

def GGH_keys(B):
    # Creem la matriu aleatoria U amb determinant +-1
    n = len(B)
    U = np.empty((n, n))
    is_found = False
    while not is_found:
        # Nota: s'ha utilitzat el rang (-10,+10) pel temps que es triga a trobar U, potser hi ha una manera millor
        U = np.random.randint(-10, 10, size = (n, n))
        if abs(np.linalg.det(U)) == 1:
            is_found = True
    # Calculem W = U x B
    W = np.dot(U, B)
    return W

def GGH_encryption(m, W):
    # Nota: per al vector aleatori utilitzem el mateix rang que abans
    r = np.random.randint(-10, 10, size = (len(m)))
    print('r:', r)
    # Calculem m x W + r
    c = np.dot(m, W) + r
    return c

def GGH_decryption(c, B, W):
    # decrypt = c x pow(B, -1) x pow(U, -1)
    # where U = W/B
    m = np.array([0]*len(c))
    cB1 = np.around(np.dot(c, np.linalg.matrix_power(B, -1)))
    U = np.around(np.dot(W, np.linalg.matrix_power(B, -1)))
    # comprovar que U te determinant +-1
    if abs(np.around(np.linalg.det(U))) == 1:
        m = np.around(np.dot(cB1, np.linalg.matrix_power(U, -1)))
    return m

def getR(c, m, W):
    r = np.subtract(c, np.dot(m, W))
    return r

# Hadamard ratio: nonorthogonality of the basis
def hadamard_ratio(B):
    # calculem la determinant de la base
    det = abs(np.linalg.det(B))
    print('det:', np.linalg.det(B))
    # calculem la ratio amb la determinant i la norma de cada vector
    ratio = math.sqrt((det/(np.linalg.norm(B[0]) * np.linalg.norm(B[1]) * np.linalg.norm(B[2]))))
    return np.around(ratio, 3)

if __name__ == '__main__':
    # Definim B
    B = np.array([[-97, 19, 19], [-36, 30, 86], [-184, -64, 78]])
    print('hadamard ratio:', hadamard_ratio(B))
    # Calculem W
    W = GGH_keys(B)
    print('private key:\n', B)
    print('public key:\n', W)
    # Xifrar missatge
    m = np.array([86, -35, -32])
    c = GGH_encryption(m, W)
    print("encrypted message:\n", c)
    # GET r
    r = getR(c, m, W)
    print('r:', r)
    # Desxifrar missatge
    m2 = GGH_decryption(c, B, W)
    print("decrypted message:\n", m2)
    if np.array_equal(m, m2):
        print("correct decryption")
    else:
        print("wrong decryption")

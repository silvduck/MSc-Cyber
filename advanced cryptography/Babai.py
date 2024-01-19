# Silvia Sanvicente, maig 2022, UOC - MUCiberSec - Advanced Cryptography

import numpy as np
import math

# Algorisme de Babai
# IN: B{v1, ..., vn} (vectors basics de L) i w (vector arbitrari)
# OUT: v (vector mes proper a w)
def babai(B, w):
    # resolem el sistema per trobar t1 i t2
    trans = B.transpose()
    t = np.linalg.inv(trans).dot(w)
    t = np.around(t)
    # calculem v
    v = t[0]*B[0] + t[1]*B[1]
    return np.array(v, dtype = 'int')

# Hadamard ratio: nonorthogonality of the basis
def hadamard_ratio(B):
    # calculem la determinant de la base
    det = abs(np.linalg.det(B))
    # calculem la ratio amb la determinant i la norma de cada vector
    ratio = math.sqrt((det/(np.linalg.norm(B[0]) * np.linalg.norm(B[1]))))
    return np.around(ratio, 3)


if __name__ == '__main__':
    # definir B i w
    B = np.array([[213, -437], [312, 105]])
    w = np.array([43127, 11349])
    # calcular v
    v = babai(B, w)
    print('v:', v)
    # calcular distancia
    dist = np.linalg.norm(v-w)
    print('distance:', np.around(dist, 2))
    # calcular hadamard ratio (no ortogonalitat)
    ratio = hadamard_ratio(B)
    print('hadamard ratio:', ratio)

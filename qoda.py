import math
from qiskit import QuantumRegister, QuantumCircuit

from qvar import QVAR
from ffqram import _encode_vectors
from util import inv_stereo

def QOF(vectors):
    M = len(vectors)
    N = len(vectors[0])

    m = math.ceil(math.log2(M))
    n = math.ceil(math.log2(N))
    t = 2*m+n                   # number of index qubits
    a_r_qubits = 1 + n + m - 2  # number of ancillas for controlled rotations

    d = QuantumRegister(1, 'd') # ancilla for the computation of differences
    r = QuantumRegister(1, 'r') # register qubit for ff-qram
    i = QuantumRegister(m, 'i') # register for indexing the first loading of the M records
    j = QuantumRegister(m, 'j') # register for indexing the second loading of the M records
    k = QuantumRegister(n, 'k') # register for indexing the N features of each records
    ancillaRotation = QuantumRegister(a_r_qubits, 'x')

    U = QuantumCircuit(d,r,k,i,j,ancillaRotation) # circuit for the computation of differences
    
    U.h(d)
    U.h(i)
    U.h(j)
    U.h(k)

    # load the M records controlled by i
    _encode_vectors(U, vectors, d, k, i, r, ancillaRotation)

    U.x(d)

    # load the M records controlled by j
    _encode_vectors(U, vectors, d, k, j, r, ancillaRotation)

    # differences computation
    U.h(d)
    
    # variance computation
    q_var = QVAR(U, var_index=list(range(2, 2+t)), version='FAE')
    
    return q_var

def QODA(X, t):

    outliers = []
    for pivot in X:
        print("pivot " + str(pivot))
        tmp_X = X - pivot
        new_pivot = pivot - pivot 
        tmp_X = [x for x in tmp_X if (x != new_pivot).any()]
        tmp_X = inv_stereo(tmp_X)
        
        var = QOF(tmp_X)
        print("variance: " + str(var))
        if var < t:
            outliers.append(pivot)

    return outliers
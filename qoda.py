import math
from qiskit import QuantumRegister, QuantumCircuit

from QVAR import QVAR
from ffqram import _encode_vectors
from util import inv_stereo

def QOF(vectors):
    M = len(vectors)
    N = len(vectors[0])

    m = math.ceil(math.log2(M))
    n = math.ceil(math.log2(N))
    t = 2*m+n                   # number of index qubits

    d = QuantumRegister(1, 'd') # ancilla for the computation of differences
    r = QuantumRegister(1, 'r') # register qubit for ff-qram
    i = QuantumRegister(m, 'i') # register for indexing the first loading of the M records
    j = QuantumRegister(m, 'j') # register for indexing the second loading of the M records
    k = QuantumRegister(n, 'k') # register for indexing the N features of each records

    U = QuantumCircuit(k,i,j,d,r) # circuit for the computation of differences
    
    U.h(d)
    U.h(i)
    U.h(j)
    U.h(k)

    # load the M records controlled by i
    _encode_vectors(U, vectors, d, k, i, r)

    U.x(d)

    # load the M records controlled by j
    _encode_vectors(U, vectors, d, k, j, r)

    # differences computation
    U.h(d)
    
    # variance computation
    q_var = QVAR(U, var_index=list(range(t)), ps_index=[U.num_qubits-1], n_h_gates=t+2)
    
    return q_var

def QODA(X, t):

    outliers = []
    q = []
    for pivot in X:
        print("pivot " + str(pivot))
        tmp_X = X - pivot
        new_pivot = pivot - pivot 
        tmp_X = [x for x in tmp_X if (x != new_pivot).any()]
        tmp_X = inv_stereo(tmp_X)
        
        var = QOF(tmp_X)
        print("variance: " + str(var))

        q.append(var)

        if var < t:
            outliers.append(pivot)

    return outliers
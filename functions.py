import numpy as np
import time
##
def gram_schmidt(M):
    A   = M.astype(float)
    m,n = A.shape
    Q   = np.zeros(shape=(m,n),dtype=float)
    R   = np.zeros(shape=(n,n),dtype=float)
    for j in range(n):
        R[:j,j] = np.dot(Q.T[:j,:], A[:,j])         #coordinates
        Q[:,j]  = A[:,j] - np.dot(Q[:,:j], R[:j,j]) #current column - projection onto previous columns
        R[j,j]  = np.sqrt(np.dot(Q[:,j],Q[:,j]))    #the diagonals of R = lengths of coordinate axes
        Q[:,j]  = Q[:,j]/R[j,j]                     #every coordinate axis scaled to length 1

    return Q,R

def test_gram_schmidt():
    np.random.seed(123)
    size = 100
    M = np.random.random((size,size))
    start = time.time()
    Q, R = gram_schmidt(M)
    print(time.time()-start)
    I_expected   = np.identity(size)
    I_observed   = np.dot(Q.T, Q)  #Are the columns of Q all orthogonal to each other?  Are they all length of 1?
    I_difference = np.sqrt(np.sum((I_expected-I_observed)**2))
    A_difference = np.sqrt(np.sum((M-(Q@R))**2)) #Does the produce of Q and R equal the original input matrix?
    return I_difference, A_difference

def orthogonal_iteration(M, nsteps=30):
    A = M.astype(float)
    m,n = A.shape
    Q = np.identity(m) #eigenvectors
    for step in range(nsteps):
        AQ = np.dot(A, Q)
        Q,R= gram_schmidt(AQ)
    '''
    Why do we just return the R as the eigenvalues?
    At convergence, AQ has every column orthogonal but not all length 1.
    Subsequent A x Q will just be scaling the columns of Q.
    If AQ = QxR, R is a matrix that scales the columns of Q.
    Therefore, R would approach a diagonal matrix containing the eigenvalues.
    '''
    return np.diag(R), Q

def test_orthogonal_iteration():
    A = np.array([
        [1,3,2,4],
        [4,5,6,2],
        [7,8,9,5],
        [5,2,7,8]    
    ])
    Q, R = gram_schmidt(A)
    eigvalues  = np.array([
        [4,0,0,0],
        [0,3,0,0],
        [0,0,2,0],
        [0,0,0,1]
    ])
    M = Q @ eigvalues @ Q.T
    print("The expected eigvals :", np.linalg.eigvals(M))
    S,X = orthogonal_iteration(M)
    print("The observed eigenvas:",  S)

def svd(M):
    A   = M.astype(float)
    m,n = A.shape
    ATA = np.dot(A.T, A)
    S,V = orthogonal_iteration(ATA)
    S   = np.sqrt(S)
    AV  = np.dot(A,V)
    U   = np.dot(AV, np.diag(1/S))
    norms = np.dot( np.ones(shape=m), U**2) 
    U     = np.dot(U, np.diag(1/norms))  #normalize
    return U,S,V

def test_svd():
    np.random.seed(123)
    m,n = 100,100
    M=np.random.random(size=(m,n))*10
    U,S,V = svd(M)
    I_expected   = np.identity(m)
    I_observed   = np.dot(U.T, U)  #Are the columns of U all orthogonal to each other?  Are they all length of 1?
    I_difference = np.sqrt(np.sum((I_expected-I_observed)**2))
    print("How close U is to orthonormal: ",I_difference)

    I_expected   = np.identity(n)
    I_observed   = np.dot(V.T, V)  #Are the columns of V all orthogonal to each other?  Are they all length of 1?
    I_difference = np.sqrt(np.sum((I_expected-I_observed)**2))
    print("How close V is to orthonormal: ",I_difference)

    print("Reconstruction Error",np.sqrt(np.sum(((U@np.diag(S)@V.T) - M)**2)))

print()
import numpy as np
from scipy.sparse import lil_matrix
from numpy.random import rand, seed
from mpi4py import MPI
import matplotlib.pyplot as plt


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

seed(0)

def matrixVectorMult(A, b, x):
    
    row, col = A.shape
    for i in range(row):
        a = A[i]
        for j in range(col):
            x[i] += a[j] * b[j]

    return 0

value = 1000
val = value//size


if rank == 0:
    A = lil_matrix((value, value))
    A[0, :100] = rand(100)
    A[1, 100:200] = A[0, :100]
    A.setdiag(rand(value))
    A = A.toarray()
    b = rand(value)
else :
    A = None
    b = None


matrix = np.zeros((val, value))
comm.Scatter(A, matrix, root=0)

b=comm.bcast(b,root=0)

valx = np.zeros(val)


start = MPI.Wtime()
matrixVectorMult(matrix, b, valx)
stop = MPI.Wtime()
if rank == 0:
    print("CPU time of matrix multiplication is ", (stop - start)*1000)

sendcounts = np.array(comm.gather(len(valx),root=0))

if rank == 0: 
    X = np.zeros(sum(sendcounts),dtype=np.double)

else :
    X = None

if rank == 0:
    print(len(X))

comm.Gatherv(valx, recvbuf=(X, sendcounts, MPI.DOUBLE), root=0)

if rank == 0 :
    X_ = A.dot(b)
    print("The result of the product A*b using dot is :", np.max(X_ - X))


CPU_time=[319.79, 161.50, 112.62]
plt.plot([1,2,4],CPU_time)
plt.title("the scalability")
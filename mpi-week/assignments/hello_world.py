from mpi4py import MPI

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()

print("hello from process ", RANK, " out of ", SIZE, " processes")
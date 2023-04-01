from mpi4py import MPI

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()

while True:
    if RANK == 0:
        num = int(input("Enter an integer: "))
    else:
        num = None
    num = COMM.bcast(num, root=0)
    if num < 0:
        break
    print("Process %d got %d" % (RANK, num))
    COMM.Barrier()

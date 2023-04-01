from mpi4py import MPI
import numpy as np

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()

value = 0
while value >= 0:
    if RANK == 0:
        value = int(input("Enter an integer: "))
        COMM.send(value, dest=RANK + 1)
    else:
        value = COMM.recv(source=RANK - 1)
        if RANK < SIZE - 1:
            COMM.send(value, dest=RANK + 1)

    print("Process %d got %d" % (RANK, value))
    COMM.Barrier()

MPI.Finalize()
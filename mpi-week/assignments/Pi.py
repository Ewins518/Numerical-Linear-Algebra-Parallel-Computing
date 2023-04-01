import random 
import timeit
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

interval= 500
nbi=int(interval/size)+(size==(rank+1))*(interval%size)

def compute_points():
    
    random.seed(42)  
    
    circle_points= 0

    for i in range(nbi): 
          
        rand_x= random.uniform(-1, 1) 
        rand_y= random.uniform(-1, 1) 
      
        origin_dist= rand_x**2 + rand_y**2
      
        if origin_dist<= 1: 
            circle_points+= 1

    return circle_points

start = timeit.default_timer()
circle_points = compute_points()
total_circle_points=comm.reduce(circle_points,op=MPI.SUM, root=0)
end = timeit.default_timer()


if rank==0:
    print("Circle points number :",circle_points)
    pi = 4* total_circle_points/ interval
    print("Pi value=", pi, "obtained in :",end-start, "seconds") 
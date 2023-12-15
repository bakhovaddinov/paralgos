from mpi4py import MPI
import numpy as np

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

vector_size = 100000

if rank == 0:
    vector1 = np.ones(vector_size)
    vector2 = 2 * np.ones(vector_size)
else:
    vector1 = np.empty(vector_size)
    vector2 = np.empty(vector_size)

MPI.COMM_WORLD.Scatter([vector1, MPI.DOUBLE], [vector1, MPI.DOUBLE], root=0)
MPI.COMM_WORLD.Scatter([vector2, MPI.DOUBLE], [vector2, MPI.DOUBLE], root=0)

partial_result = np.multiply(vector1, vector2)

total_result = np.empty(vector_size)
MPI.COMM_WORLD.Reduce([partial_result, MPI.DOUBLE], [total_result, MPI.DOUBLE], op=MPI.SUM, root=0)

if rank == 0:
    dot_product = np.sum(total_result)
    print(f"The dot product is: {dot_product}")

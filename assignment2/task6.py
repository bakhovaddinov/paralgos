from mpi4py import MPI
import numpy as np
import sys
import time

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

num_elements = 1
increase_by = 1000
max_elements = 50000
num_repeats = 10

while num_elements <= max_elements:
    data = [0] * num_elements
    object_size = sys.getsizeof(data)

    for _ in range(num_repeats):
        if rank == 0:
            MPI.COMM_WORLD.send(data, dest=1, tag=0)
        elif rank == 1:
            received_data = MPI.COMM_WORLD.recv(source=0, tag=0)

    start_time = time.time()
    for _ in range(num_repeats):
        if rank == 0:
            MPI.COMM_WORLD.send(data, dest=1, tag=0)
        elif rank == 1:
            received_data = MPI.COMM_WORLD.recv(source=0, tag=0)
    end_time = time.time()

    elapsed_time = end_time - start_time
    bandwidth = (2 * num_repeats * object_size) / (elapsed_time * 1024 * 1024)

    if rank == 0:
        print(f"{object_size} bytes: {bandwidth:.2f} MB/s")

    num_elements += increase_by

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Worker logic
worker_data = {'rank': rank}
print(f"Worker {rank} created. Sending message to Host.")
comm.send(worker_data, dest=0, tag=0)

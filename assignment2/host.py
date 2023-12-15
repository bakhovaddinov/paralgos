from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    # Master (host) logic
    for worker_rank in range(1, size):
        worker_data = comm.recv(source=worker_rank, tag=0)
        print(f"Host received message from Worker {worker_data['rank']}: {worker_data}")
else:
    # Worker logic
    worker_data = {'rank': rank}
    print(f"Worker {rank} created. Sending message to Host.")
    comm.send(worker_data, dest=0, tag=0)

from mpi4py import MPI

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

if rank != 0:
    message = f"Hello from Worker {rank}!"
    start_time = MPI.Wtime()
    MPI.COMM_WORLD.send(message, dest=0, tag=rank)
    end_time = MPI.Wtime()
    elapsed_time = (end_time - start_time) * 1000
    print(f"Worker {rank} sent message in {elapsed_time:.2f} milliseconds.")

if rank == 0:
    for worker_rank in range(1, size):
        start_time = MPI.Wtime()
        message = MPI.COMM_WORLD.recv(source=worker_rank, tag=worker_rank)
        end_time = MPI.Wtime()
        elapsed_time = (end_time - start_time) * 1000
        print(f"Host received message from Worker {worker_rank} in {elapsed_time:.2f} milliseconds.")

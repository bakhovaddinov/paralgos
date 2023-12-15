from mpi4py import MPI
import time

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

if rank == 0:
    for _ in range(1, size):
        message = MPI.COMM_WORLD.recv(source=MPI.ANY_SOURCE, tag=0)
        print(f"Host received message from Worker {message['rank']}: '{message['content']}'")

if rank != 0:
    message = {'rank': rank, 'content': f"Hello from Worker {rank}!"}
    MPI.COMM_WORLD.send(message, dest=0, tag=0)
    print(f"Worker {rank} sent message and continues running.")
    time.sleep(5)
    print(f"Worker {rank} finished.")

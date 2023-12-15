from mpi4py import MPI

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

if size != 10:
    if rank == 0:
        print("Please run the program with exactly 10 processes.")
    MPI.COMM_WORLD.Abort()

original_message = "Hello from the host!"

if rank == 0:
    MPI.COMM_WORLD.send(original_message, dest=1, tag=0)
    received_message = MPI.COMM_WORLD.recv(source=size - 1, tag=0)
    print(f"Host received message: '{received_message}'")
    print("DONE")

else:
    received_message = MPI.COMM_WORLD.recv(source=rank - 1, tag=0)
    print(f"Worker {rank} received message from Worker {rank - 1}: '{received_message}'")
    MPI.COMM_WORLD.send(original_message, dest=(rank + 1) % size, tag=0)

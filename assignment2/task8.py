from mpi4py import MPI
import time

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

if rank == 0:
    message = "Hello from the host!"
    request = MPI.COMM_WORLD.isend(message, dest=1, tag=0)

    waiting_message_count = 0
    while True:
        time.sleep(5)
        waiting_message_count += 5
        print(f"Host: Waiting for confirmation ({waiting_message_count} seconds elapsed)")

        status = MPI.Status()
        if MPI.COMM_WORLD.Iprobe(source=1, tag=0):
            request.Wait()
            break

    print("Host: Message received by Worker 1")
else:
    time.sleep(25)
    status = MPI.Status()
    received_message = MPI.COMM_WORLD.recv(source=0, tag=0, status=status)
    print(f"Worker {rank}: Received message: '{received_message}'")
    MPI.COMM_WORLD.send("Message received", dest=0, tag=0)

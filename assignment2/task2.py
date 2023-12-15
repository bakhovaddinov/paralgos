from mpi4py import MPI
import numpy as np

class Person:
    def __init__(self, name, age, occupation):
        self.name = name
        self.age = age
        self.occupation = occupation

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

object1 = [1, 2, 3]  
object2 = np.array([4, 5, 6])  
iskandar_data = Person(name="Iskandar", age=22, occupation="Engineer")

list_of_objects = [object1, object2, iskandar_data]

if rank == 0:
    for i in range(1, size):
        comm.send(list_of_objects[i - 1], dest=i, tag=i)

if rank != 0:
    received_object = comm.recv(source=0, tag=rank)

    if isinstance(received_object, Person):
        print(f"Worker {rank} received Person object: Name: {received_object.name}, Age: {received_object.age}, Occupation: {received_object.occupation}")
    else:
        print(f"Worker {rank} received object: {received_object}")

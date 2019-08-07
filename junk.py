from queue import Queue
from threading import Thread

def f1():
    print('Function one')

def f2():
    print('Function two')

t1 = Thread(target=f1)
t2 = Thread(target=f2)

print(dir(t1))
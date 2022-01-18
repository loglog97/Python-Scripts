import threading
import time
from queue import Queue
import string
import random

"""
Producer-Consumer problem (or the bounded-buffer problem)
By: Logan Cole

Problem: Two processes (the producer and consumer) who share a common
fixed sized buffer used as a queue. The producer's job is to generate data,
put it into the buffer, and start again. At the same time, the consumer is taking the data
one at a time. 

Solution: Either the producer goes to sleep or discard data if the buffer is full.
When the consumer takes an item away, it should notify the producer. If the buffer is
empty, the consumer goes to sleep. When the producer puts data in the buffer, it wakes
the consumer.

Mistakes made:
1. Named the file threading.py which cause issues running. Took me 20 minutes to figure out why(thanks stackoverflow)
"""

itemCount = 0
BUFFER_SIZE = 10
q = Queue(maxsize = 10)
lock = threading.Lock()
producerResult = threading.Event()
consumerResult = threading.Event()
#result_available.set()
#result_available.wait()

def produceItem():
    item = random.choice(string.ascii_letters)
    return item

def producer():
    global itemCount
    if(q.full()):
        print('waiting for consumer')
        consumerResult.wait()
    with lock: #locks the thread so only one can access at a time
        if(itemCount < 10):
            item = produceItem()
            print("item produced")
            print(item)
            q.put(item) #places an item in the queue
            itemCount+=1
        if(q.empty()):
            producerResult.set()

def consumer():
    global itemCount
    if(q.empty()):
        print('waiting for producer')
        producerResult.wait()
    with lock:
        if(itemCount > 0):
            item = q.get() #takes item from queue
            print(item)
            print('item taken from queue')
            itemCount-=1
        if(q.full()):
            consumerResult.set()

def main():
    counter = 0
    while counter != 100: 
        producer()
        consumer()
        counter += 1
        print(counter)
    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    
main()


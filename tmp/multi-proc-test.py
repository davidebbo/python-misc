import logging
from multiprocessing import Pool
import os
import sys
import time

def f(x):
    # Print the process ID
    print(f'Process ID: {os.getpid()}, x: {x}')

    # Run some logic that uses up some CPU time
    for i in range(100000000):
        x*x

    print(f'Process ID: {os.getpid()}. Done!')

    return x*x

if __name__ == '__main__':

    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    input = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    start = time.time()
    with Pool(10) as p:
        for result in p.imap_unordered(f, input):
            print(result)
    
    end = time.time()
    logging.debug("Time taken parallel: {} seconds".format(end - start))
    
    start = time.time()
    for i in input:
        f(i)
    end = time.time()
    logging.debug("Time taken sync: {} seconds".format(end - start))
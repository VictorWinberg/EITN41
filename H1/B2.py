import hashlib
import binascii
import math
import numpy
import time
import os
from sys import argv
from random import randint

def micromint(u, k, c):
    """ Makes MicroMint coins.
    Args:
        u (int): Bits.
        k (int): Collisions.
        c (int): Coins.
    """
    bins = [[] for x in range(2**u)]

    coins = []
    tries = 0
    while len(coins) < c:
        x = os.urandom(u)
        y = sha1(x, math.floor(u / 8))
        i = bytes_to_int(y)
        bins[i].append(x)
        if len(bins[i]) == k:
            coins.append(bins[i])
        tries += 1
    return tries, coins

def mean_and_width(x):
    mean = numpy.mean(x)
    s = numpy.std(x)
    n = len(x)
    _lambda = 3.66
    width = 2 * _lambda * s / math.sqrt(n) if n > 1 else float('inf')
    return mean, width

def sha1(x, b):
    return hashlib.sha1(x).digest()[:b]

def bytes_to_int(x, byteorder='big'):
    return int.from_bytes(x, byteorder)

if __name__ == "__main__":
    if len(argv) == 4:
        u, k, c = map(int, argv[1:])
        tries, coins = micromint(u, k, c)
        print(tries)
    elif len(argv) == 5:
        u, k, c, ci_width = map(int, argv[1:])
        all_tries = []
        t = time.time()
        while True:
            tries, coins = micromint(u, k, c)
            all_tries.append(tries)
            mean, width = mean_and_width(all_tries)
            if time.time() - t > 30:
                t = time.time()
                print(mean, width)
            if width <= ci_width:
                break

        print(mean, width)

    # Debugging
    import pdb
    debug = input("Debug (y/N)? ")

    if(debug == 'y' or debug == 'yes'):
        pdb.set_trace()

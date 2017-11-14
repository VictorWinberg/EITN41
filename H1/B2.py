import hashlib
import binascii
import math
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
        x = os.urandom(2*u)
        y = sha1(x, math.floor(u / 8))
        i = bytes_to_int(y)
        bins[i].append(x)
        if len(bins[i]) == k:
            coins.append(bins[i])
        tries += 1
    return tries, coins

def sha1(x, b):
    return hashlib.sha1(x).digest()[:b]

def bytes_to_int(x, byteorder='big'):
    return int.from_bytes(x, byteorder)

if __name__ == "__main__":
    if len(argv) == 4:
        tries, coins = micromint(*map(int, argv[1:]))
    elif len(argv) == 5:
        result = [micromint(*map(int, argv[1:4])) for x in range(int(argv[4]))]
        tries, coins = list(zip(*result))
        print('x_mean', sum(tries)/len(tries))

    # Debugging
    import pdb
    debug = input("Debug (y/N)? ")

    if(debug == 'y' or debug == 'yes'):
        pdb.set_trace()

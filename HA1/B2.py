import binascii
import hashlib
import math
import numpy
import os
import time
from sys import argv

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
    y = hash(x, u)
    i = (int(y, 16) if u % 4 == 0 else y)
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

def hash(x, u):
  h = hashlib.sha1(x).hexdigest()
  if u % 4 == 0:
    return h[:u//4]
  else:
    return int(h, 16) % 2**u

if __name__ == "__main__":
  if len(argv) == 1:
    argv = ['B2.py', '16', '2', '1', '22']

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

    print(mean, width, len(all_tries))

  # Debugging
  import pdb
  debug = input("Debug (y/N)? ")

  if(debug == 'y' or debug == 'yes'):
    pdb.set_trace()

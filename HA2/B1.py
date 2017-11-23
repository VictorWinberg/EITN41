import binascii
import hashlib
from sys import argv
from random import randrange, sample
from functools import reduce

def DCnet(SA, SB, DA, DB, M, b):
  if b == 0:
    D = SA ^ SB
    M = DA ^ DB ^ D

    return hex(D << 16 | M)
  elif b == 1:
    return hex(SA ^ SB ^ M)
  else:
    return 'Incorrect values'

if __name__ == "__main__":
  try:
    OUT = DCnet(*[int(input().split(' ')[1], 16) for x in range(6)])
    print(OUT.upper()[2:])
  except EOFError:
    pass

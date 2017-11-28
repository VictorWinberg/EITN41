import binascii
import hashlib
import os
from functools import reduce

def rand(K = 16):
  return os.urandom(K // 8)

def hash(v, k, X):
  h = hashlib.sha1(v+k).hexdigest()
  return int(h, 16) % 2**X

def toByte(x, byteorder='big'):
  length = x.bit_length() // 8 + 1
  return x.to_bytes(length, byteorder)

def binding_probability(X, K = 16):
  x = hash(b'0', rand(), X)
  h = -1

  for i in range(2 ** K):
    h = hash(b'1', toByte(i), X)
    if x == h:
      return 1

  return 0

def concealing_probability(X, K = 16):
  v = b'0'
  x = hash(v, rand(), X)
  correct, incorrect = 0, 0

  for i in range(2 ** K):
    h0 = hash(b'0', toByte(i), X)
    h1 = hash(b'1', toByte(i), X)

    if x == h0: correct += 1
    if x == h1: incorrect += 1

  if correct + incorrect == 0:
    return 0

  return correct / (correct + incorrect)


X = 20
sim = 10

binding = [binding_probability(X) for i in range(sim)]
print(sum(binding) / len(binding))

concealing = [concealing_probability(X) for i in range(sim)]
print(sum(concealing) / len(concealing))

# Debugging
import pdb
debug = input("Debug (y/N)? ")

if(debug == 'y' or debug == 'yes'):
  pdb.set_trace()

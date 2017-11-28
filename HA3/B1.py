import binascii
import hashlib
import os
import matplotlib.pyplot as plt
from functools import reduce

def commitment(v, k, X):
  h = hashlib.sha1(v+k).hexdigest()
  return int(h, 16) % 2 ** X

def toByte(x, byteorder = 'big', K = 16):
  return x.to_bytes(K // 8, byteorder)

def binding_probability(X, K = 16):
  x = commitment(b'0', os.urandom(K // 8), X)

  for i in range(2 ** K):
    if x == commitment(b'1', toByte(i), X):
      return 1

  return 0

def concealing_probability(X, K = 16):
  x = commitment(b'0', os.urandom(K // 8), X)
  correct, incorrect = 0, 0

  for i in range(2 ** K):
    if x == commitment(b'0', toByte(i), X):
      correct += 1
    if x == commitment(b'1', toByte(i), X):
      incorrect += 1

  return correct / (correct + incorrect)

size = 30
res = 10
bindings, concealings = [], []

for X in range(size):
  binding = [binding_probability(X) for i in range(res)]
  bindings.append(sum(binding) / len(binding))

  concealing = [concealing_probability(X) for i in range(res)]
  concealings.append(sum(concealing) / len(concealing))

  print(X / size)

plt.plot(range(size), bindings, label='binding')
plt.plot(range(size), concealings, label='concealing')

plt.xlabel('X')

plt.axhline(y = 0, color='k')
plt.axvline(x = 0, color='k')

plt.legend(loc = 'upper right')

plt.show()

# Debugging
import pdb
debug = input("Debug (y/N)? ")

if(debug == 'y' or debug == 'yes'):
  pdb.set_trace()

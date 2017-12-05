import math
import hashlib
import binascii
from functools import reduce

def I2OSP(x, xLen):
  """ Converts (nonnegative) integer to bytes
  Input:
    x    - nonnegative integer to be converted
    xLen - intended length of the resulting bytes
  Output:
    X (bytes)
   Error:  "integer too large"
  """
  if x >= 256 ** xLen: raise Exception("integer too large")

  # Alt: The simple one-liner
  # bytes([x >> (8 * i) & 0xFF for i in range(xLen)[::-1]])
  
  X = []
  for i in range(xLen):
    X.append(x % 256)
    x = x // 256

  return bytes(X[::-1])
  

def MGF1(mgfSeed, maskLen, Hash=hashlib.sha1, hLen=20):
  """ Mask Generation Function based on a hash function
  Input:
    mgfSeed (hexadecimal) - mask seed
    maskLen (decimal)     - mask length in bytes
  Output:
    mask (hexadecimal)
  Error: "mask too long"
  """
  if maskLen > 2 ** 32 * hLen: raise Exception("mask too long")
  mgfSeed = binascii.unhexlify(mgfSeed)

  T = bytes()
  for counter in range(math.ceil(maskLen / hLen)):
    C = I2OSP(counter, 4)
    T += Hash(mgfSeed + C).digest()

  return binascii.hexlify(T[:maskLen]).decode('utf-8')
  
mgfSeed = '0123456789abcdef'
maskLen = 30

print(MGF1(mgfSeed, maskLen))

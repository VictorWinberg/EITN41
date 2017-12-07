import math
from hashlib import sha1
from binascii import unhexlify,hexlify
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

def MGF1(mgfSeed, maskLen, Hash=sha1, hLen=20):
  """ Mask Generation Function based on a hash function
  Input:
    mgfSeed (bytes)   - mask seed
    maskLen (decimal) - mask length in bytes
  Output:
    mask (bytes)
  Error: "mask too long"
  """
  if maskLen > 2 ** 32 * hLen: raise Exception("mask too long")

  T = bytes()
  for counter in range(math.ceil(maskLen / hLen)):
    C = I2OSP(counter, 4)
    T += Hash(mgfSeed + C).digest()

  return T[:maskLen]

def OAEP_encode(M, seed, Hash=sha1, hLen=20, k=128):
  """ EME-OAEP encoding
  Input:
    M    (bytes) - the message to be encoded
    seed (bytes)
  Output:
    EM   (bytes) - the encoded message
  """
  L = b''
  lHash = Hash(L).digest()

  PS = I2OSP(0, k - len(M) - 2 * hLen - 2)
  DB = lHash + PS + I2OSP(1, 1) + M

  seed # given
  dbMask = MGF1(seed, k - hLen - 1)
  maskedDB = bytes(a ^ b for a,b in zip(DB, dbMask))
  seedMask = MGF1(maskedDB, hLen)
  maskedSeed = bytes(a ^ b for a,b in zip(seed, seedMask))

  EM = I2OSP(0, 1) + maskedSeed + maskedDB
  return EM

def OAEP_decode(EM, Hash=sha1, hLen=20, k=128):
  """ EME-OAEP decoding
  Input:
    EM (bytes) - the encoded message to be decoded
  Output:
    M  (bytes) - the decoded message
  """
  L = b''
  lHash = Hash(L).digest()

  Y, maskedSeed, maskedDB = EM[:1], EM[1:hLen + 1], EM[hLen + 1:]
  if not Y == b'\x00': raise Exception("decryption error")

  seedMask = MGF1(maskedDB, hLen)
  seed = bytes(a ^ b for a,b in zip(maskedSeed, seedMask))
  dbMask = MGF1(seed, k - hLen - 1)

  DB = bytes(a ^ b for a,b in zip(maskedDB, dbMask))
  flag = next((i for i, x in enumerate(DB[hLen:]) if x), None)
  if not flag: raise Exception("decryption error")
  M = DB[hLen + flag + 1:]
  return M

def hprint(t, b):
  print(t + ':', hexlify(b).decode('utf-8'), '\n')

if __name__ == '__main__':
  mgfSeed, maskLen = unhexlify(input().split('=')[1]), int(input().split('=')[1])
  M, seed, EM = map(unhexlify, [input().split('=')[1] for i in range(3)])

  calc_T = MGF1(mgfSeed, maskLen)
  hprint('T', calc_T)

  calc_EM = OAEP_encode(M, seed)
  hprint('EM', calc_EM)

  calc_M = OAEP_decode(EM)
  hprint('M', calc_M)

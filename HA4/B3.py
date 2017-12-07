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
    mgfSeed (hexadecimal) - mask seed
    maskLen (decimal)     - mask length in bytes
  Output:
    mask (hexadecimal)
  Error: "mask too long"
  """
  if maskLen > 2 ** 32 * hLen: raise Exception("mask too long")
  mgfSeed = unhexlify(mgfSeed)

  T = bytes()
  for counter in range(math.ceil(maskLen / hLen)):
    C = I2OSP(counter, 4)
    T += Hash(mgfSeed + C).digest()

  return hexlify(T[:maskLen]).decode('utf-8')

def OAEP_encode(M, seed, Hash=sha1, hLen=20, k=128):
  """ EME-OAEP encoding
  Input:
    M - the message to be encoded
    seed
  Output:
    EM - the encoded message
  """
  M, seed = map(unhexlify, (M, seed))
  L = b''
  lHash = Hash(L).digest()

  PS = I2OSP(0, k - len(M) - 2 * hLen - 2)
  DB = lHash + PS + I2OSP(1, 1) + M

  seed # given
  dbMask = unhexlify(MGF1(hexlify(seed), k - hLen - 1))
  maskedDB = bytes(a ^ b for a,b in zip(DB, dbMask))
  seedMask = unhexlify(MGF1(hexlify(maskedDB), hLen))
  maskedSeed = bytes(a ^ b for a,b in zip(seed, seedMask))

  EM = I2OSP(0, 1) + maskedSeed + maskedDB
  return hexlify(EM).decode('utf-8')

def OAEP_decode(EM):
  """ EME-OAEP decoding
  Input:
    EM - the encoded message to be decoded
  Output:
    M - the decoded message
  """
  # a.  If the label L is not provided, let L be the empty string.
  #     Let lHash = Hash(L), an octet string of length hLen (see
  #     the note in Section 7.1.1).
  # 
  # b.  Separate the encoded message EM into a single octet Y, an
  #     octet string maskedSeed of length hLen, and an octet
  #     string maskedDB of length k - hLen - 1 as
  # 
  #        EM = Y || maskedSeed || maskedDB.
  # 
  # c.  Let seedMask = MGF(maskedDB, hLen).
  # 
  # d.  Let seed = maskedSeed \xor seedMask.
  # 
  # e.  Let dbMask = MGF(seed, k - hLen - 1).
  # 
  # f.  Let DB = maskedDB \xor dbMask.
  # 
  # g.  Separate DB into an octet string lHash' of length hLen, a
  #     (possibly empty) padding string PS consisting of octets
  #     with hexadecimal value 0x00, and a message M as
  # 
  #        DB = lHash' || PS || 0x01 || M.
  # 
  #     If there is no octet with hexadecimal value 0x01 to
  #     separate PS from M, if lHash does not equal lHash', or if
  #     Y is nonzero, output "decryption error" and stop.  (See
  #     the note below.)

mgfSeed = '0123456789abcdef'
maskLen = 30
T = '18a65e36189833d99e55a68dedda1cce13a494c947817d25dc80d9b4586a'

M = 'fd5507e917ecbe833878'
seed = '1e652ec152d0bfcd65190ffc604c0933d0423381'
EM = '0000255975c743f5f11ab5e450825d93b52a160aeef9d3778a18b7aa067f90b2178406fa1e1bf77f03f86629dd5607d11b9961707736c2d16e7c668b367890bc6ef1745396404ba7832b1cdfb0388ef601947fc0aff1fd2dcd279dabde9b10bfc51f40e13fb29ed5101dbcb044e6232e6371935c8347286db25c9ee20351ee82'

calc_T = MGF1(mgfSeed, maskLen)
print('correct:', T == calc_T, calc_T)
calc_EM = OAEP_encode(M, seed)
print('correct:', calc_EM == EM, calc_EM)

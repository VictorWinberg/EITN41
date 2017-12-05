import math
import hashlib
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
  mgfSeed = unhexlify(mgfSeed)

  T = bytes()
  for counter in range(math.ceil(maskLen / hLen)):
    C = I2OSP(counter, 4)
    T += Hash(mgfSeed + C).digest()

  return hexlify(T[:maskLen]).decode('utf-8')

def OAEP_encode(M, seed, Hash=hashlib.sha1):
  """ EME-OAEP encoding
  Input:
    M - the message to be encoded
    seed
  Output:
    EM - the encoded message
  """
  # a.  If the label L is not provided, let L be the empty string.
  #     Let lHash = Hash(L), an octet string of length hLen (see
  #     the note below).
  #
  # b.  Generate a padding string PS consisting of k - mLen -
  #     2hLen - 2 zero octets.  The length of PS may be zero.
  #     c.  Concatenate lHash, PS, a single octet with hexadecimal
  #     value 0x01, and the message M to form a data block DB of
  #     length k - hLen - 1 octets as
  # 
  #        DB = lHash || PS || 0x01 || M.
  # 
  # d.  Generate a random octet string seed of length hLen.
  # 
  # e.  Let dbMask = MGF(seed, k - hLen - 1).
  # 
  # f.  Let maskedDB = DB \xor dbMask.
  # 
  # g.  Let seedMask = MGF(maskedDB, hLen).
  # 
  # h.  Let maskedSeed = seed \xor seedMask.
  # 
  # i.  Concatenate a single octet with hexadecimal value 0x00,
  #     maskedSeed, and maskedDB to form an encoded message EM of
  #     length k octets as
  # 
  #        EM = 0x00 || maskedSeed || maskedDB.

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

print(MGF1(mgfSeed, maskLen))

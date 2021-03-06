import binascii
import hashlib
from sys import argv
from random import randrange, sample
from functools import reduce

def get_n(p, q):
  return p * q

def totient(p, q):
  return (p - 1) * (q - 1)

def modinv_x(x, a, n):
  x = toInt(x) if type(x) != int else x
  return hex(modinv(a, n) * x % n)

# (a * a_inv) == 1 (mod n) => a_inv = modinv(a) (mod n)
# copied from https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
def modinv(a, n):
  g, x, _ = euc_algorithm(a, n)
  if g == 1:
    return x % n

# copied from https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
def euc_algorithm(a, n):
  x0, x1, y0, y1 = 1, 0, 0, 1
  while n != 0:
    q, a, n = a // n, n, a % n
    x0, x1 = x1, x0 - q * x1
    y0, y1 = y1, y0 - q * y1
  return a, x0, y0

# Encryption, decryption and blind signatures
def encrypt(m, e, n):
  m_int = byte_to_int(m.encode('utf-8'))
  if m_int != m_int % n:
    raise Exception('Max length of message exceeded')

  c_int = pow(m_int, e, n)
  c = int_to_byte(c_int).decode('latin-1')
  return c

def decrypt(c, e, n, d):
  c_int = byte_to_int(c.encode('latin-1'))
  m_int = pow(c_int, d, n)
  return int_to_byte(m_int).decode('utf-8')

def hash(x):
  x = hex(x) if type(x) == int else x
  return hashlib.sha1(x.encode('utf-8')).hexdigest()

def blind_hash(x, r, e, n):
  hash_x = toInt(hash(x))
  return hex(pow(r, e) * hash_x % n)

def blind(x, r, e, n):
  return hex(pow(r, e) * x % n)

def sign(x, n, d):
  x = toInt(x) if type(x) != int else x
  return hex(pow(x, d, n))

def verify(x, signature, e, n):
  x, signature = toInt(x), toInt(signature)
  return x == pow(signature, e, n)

def blind_signature(m, r, e, n, d):
  h_blind = blind_hash(m, r, e, n)
  h_blind_signed = sign(h_blind, n, d)
  return modinv_x(h_blind_signed, r, n)

# Converters
def byte_to_int(x, byteorder='big'):
  return int.from_bytes(x, byteorder)

def int_to_byte(x, byteorder='big'):
  length = (x.bit_length() + 7) // 8
  return x.to_bytes(length, byteorder)

def toInt(x):
  return int(x, 16)

def mul_sum(array):
  return reduce(lambda x, y: x * y % n, array)

def f(x, y):
  return x * y

def find_prime_factors(n):
  i = 2
  p = n
  while i * i <= p:
    if n % i:
      i += 1
    else:
      p //= i
  q = n // p
  return p, q

if __name__ == "__main__":
  if len(argv) == 4:
    p, q, e = map(int, argv[1:])
  else:
    p, q = 671998030559713968361666935769, 282174488599599500573849980909
    e = 17

  # Get the value n and private key d
  n = get_n(p, q)
  d = modinv(e, totient(p, q))
  print('e:', e, '\nn:', n, '\nd:', d)

  # Blind signature
  m = 'Give 10 coins!'
  blind_sign = blind_signature(m, 7, e, n, d)
  print('\nm:', m, '\nsign:', blind_sign)
  print('verified:', verify(hash(m), blind_sign, e, n), '\n')

  #
  # Improved protocol, withdrawal
  #
  # Alice chooses 2k quadruples
  ID = 1234
  print('ID:', ID)
  k, XY, quadruples, B = 8, [], [], []
  for i in range(2 * k):
    a, c, _d, r = [ randrange(1, 10 ** 20) for i in range(4) ]
    x, y = toInt(hash(a + c)), toInt(hash(a ^ ID + _d))
    b = pow(r, e) * f(x, y) % n
    B.append(b), quadruples.append([a, c, _d, r]), XY.append([x, y])

  # Bank uses cut-and-choose
  R = sample(range(len(B)), len(B) // 2)
  notR = [ i for i in range(len(B)) if i not in R ]

  # Bank verifies half of the R values
  B_bank = [0] * len(B)
  for i in R:
    a, c, _d, r = quadruples[i]
    x, y = toInt(hash(a + c)), toInt(hash(a ^ ID + _d))
    B_bank[i] = pow(r, e) * f(x, y) % n

  print('Bank verified:', all(B[i] == B_bank[i] for i in R))

  # Bank then signs the other half of the R values
  B_sign = [B[i] for i in notR]
  S_blind = pow(mul_sum(B_sign), d, n)

  # Alice calculates S without blind values
  R_arr = [quadruples[i][3] for i in notR]
  _R = mul_sum(R_arr)

  # S = modinv_x(S_blind, R, n)
  S = modinv(_R, n) * S_blind % n
  print('S:', hex(S))

  # Alice verifies by adding all x, y values included in sign
  F_arr = [f(*XY[b]) % n for b in notR]
  F = mul_sum(F_arr)

  print('Alice verifies:', F == pow(S, e, n))

  # Debugging
  import pdb
  debug = input("Debug (y/N)? ")

  if(debug == 'y' or debug == 'yes'):
    pdb.set_trace()

#
# Could be used to convert RSA base64 keys
#
# def b64_to_int(x):
#   return byte_to_int(binascii.a2b_base64(x))
#
# def int_to_b64(x):
#   return binascii.b2a_base64(int_to_byte(x))

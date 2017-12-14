from random import randrange
from hashlib import sha1

def modinv(a, n):
  g, x, _ = euc_algorithm(a, n)
  if g == 1:
    return x % n

def euc_algorithm(a, n):
  x0, x1, y0, y1 = 1, 0, 0, 1
  while n != 0:
    q, a, n = a // n, n, a % n
    x0, x1 = x1, x0 - q * x1
    y0, y1 = y1, y0 - q * y1
  return a, x0, y0

def hex2(x):
  return '{}{:x}'.format('0' * (len(hex(x)) % 2), x)

def read_buffer():
  lines = []
  while True:
    try:
      lines.append(input())
    except EOFError:
      break
  return lines

# from https://github.com/eit-lth/Advanced-Web-Security_EITN41/blob/master/5%20Data%20Representation%20and%20PKI/code/jacobi.py
def jacobi(a, m):
  j = 1
  a %= m
  while a:
  	t = 0
  	while not a & 1:
  		a = a >> 1
  		t += 1
  	if t & 1 and m % 8 in (3, 5):
  		j = -j
  	if (a % 4 == m % 4 == 3):
  		j = -j
  	a, m = m % a, a
  return j if m == 1 else 0

def rec_hash(identity, n):
  H = sha1(identity)
  a_byte, a_hex = H.digest(), H.hexdigest()
  residue = jacobi(int(a_hex, 16), n)
  return a_hex if residue == 1 else rec_hash(a_byte, n)

if __name__ == '__main__':
  p, q, identity = [ input().split(':')[1].strip() for x in ['p', 'q', 'id'] ]

  p, q = map(lambda x: int(x, 16), (p, q))
  identity = identity.encode()

  n = p * q
  a = int(rec_hash(identity, n), 16)

  r = pow(a, (n + 5 - (p + q)) // 8, n)

  print('r:', hex2(r))

  lines = read_buffer()

  decrypt = [ jacobi(int(s, 16) + 2*r, n) for s in lines ]

  decode = int(''.join(map(lambda x: '1' if x == 1 else '0', decrypt)), 2)
  print('msg:', decode)

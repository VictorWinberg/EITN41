from binascii import unhexlify
from base64 import b64encode
from sys import argv

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

def totient(p, q):
  return (p - 1) * (q - 1)

def hex2(x):
  return '{}{:x}'.format('0' * (len(hex(x)) % 2), x)

def der_encode(x):
  hex_x = hex2(x)
  if int(hex_x[0], 16) >= 0b1000:
    # signed representation of two’s complement
    hex_x = '00' + hex_x

  # Tag 0x02 INTEGER
  der = '02{}{}'.format(length_encode(hex_x), hex_x)
  return der

def length_encode(x):
  length = hex2(len(x) // 2)
  if len(x) >= 0b10000000:
    # Long definite form
    return '8' + str(len(length) // 2) + length
  else:
    # Short definite form
    return '{:02x}'.format(len(x) // 2)

def der_sequence(L):
  seq = ''.join(L)
  # Tag 0x30 SEQUENCE
  return unhexlify('30' + length_encode(seq) + seq)

if __name__ == "__main__":
  if len(argv) == 1:
    print("missing params: py B3.py der/rsa [optional]")

  elif argv[1] == 'der':
    x = int(input('x (decimal): '))
    print(der_encode(x))

  elif argv[1] == 'rsa':
    e, p, q = map(int, [ input(x + ': ') for x in ['e', 'p', 'q'] ])

    n = p * q
    d = modinv(e, totient(p, q))
    e1 = d % (p - 1)
    e2 = d % (q - 1)
    coeff = modinv(q, p)

    params = [0, n, e, d, p, q, e1, e2, coeff]

    DER = [ der_encode(param) for param in params ]
    rsa_seq = der_sequence(DER)
    print(b64encode(rsa_seq).decode('utf-8').strip())

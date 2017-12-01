from functools import reduce
from sys import argv

def mul_sum(array, n):
  return reduce(lambda x, y: x * y % n, array)

def get_n(p, q):
  return p * q

def totient(p, q):
  return (p - 1) * (q - 1)

# (a * a_inv) == 1 (mod n) => a_inv = modinv(a) (mod n)
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

def L(x, n):
  return (x - 1) / n

def micro(g, _lambda, n):
  return modinv(L(pow(g, _lambda, n**2), n), n)

def decrypt(c, _lambda, _micro, n):
  return L(pow(c, _lambda, n**2), n) * _micro % n

if __name__ == "__main__":
  p, q, g = [int(input().split('=')[1]) for i in range(3)]

  # Compute n and totient
  n = get_n(p, q)
  _lambda = totient(p, q)

  # Modular multiplication inverse
  _micro = micro(g, _lambda, n)

  if len(argv) < 2: raise Exception("Please specify an input file")
  filepath = argv[1]
  c_input = list(map(int, open(filepath).read().splitlines()))
  c = mul_sum(c_input, n ** 2)

  v = int(decrypt(c, _lambda, _micro, n))
  print(v, v - n)

  if v > len(c_input):
    v -= n

  print(v, 'mod', n)

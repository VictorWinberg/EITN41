from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from base64 import b64decode
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

if __name__ == "__main__":
  if len(argv) == 1:
    argv = ['B1.py', 'input/censored.pem', 'input/message.b64']

  pem_file, ciphertext_b64 = argv[1:]
  pem_file = open(pem_file,'rb')
  key = RSA.importKey(pem_file.read())

  p, q, e = key.p, key.q, key.e
  n = p * q
  d = modinv(e, totient(p, q))

  key = PKCS1_v1_5.new(RSA.construct((n, e, d, p, q)))

  ciphertext_b64 = open(ciphertext_b64, 'r').read()
  ciphertext = b64decode(ciphertext_b64)

  decrypted = key.decrypt(ciphertext, None).decode('utf-8')

  print(decrypted)

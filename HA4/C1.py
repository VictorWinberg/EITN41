from hashlib import sha1
from random import randrange
from binascii import unhexlify, hexlify
from functools import reduce
from sys import argv
import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("eitn41.eit.lth.se", 1337))

def recv():
  return soc.recv(4096).decode('utf-8').strip()

def recv_int():
  return int(recv(), 16)

def send(x):
  soc.send(format(x, 'x').encode('utf-8'))

def base256(L):
  return reduce(lambda x, y: int(x) << 8 | int(y), L)

def I2OSP(x, xLen = None):
  if not xLen: xLen = (x.bit_length() + 7) // 8
  return bytes([x >> (8 * i) & 0xFF for i in range(xLen)[::-1]])

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

def otr_smp(p, g, g1, msg, passphrase):
  ##########################
  #### D-H Key Exchange ####
  ##########################
  g_x1 = recv_int()
  print ('\nreceived g_x1')

  x2 = randrange(2, p)
  g_x2 = pow(g, x2, p)
  send(g_x2)
  print ('\nsent g_x2:', recv())

  DH_key = I2OSP(pow(g_x1, x2, p))

  ##########################
  ########## SMP ###########
  ##########################
  g1_a2 = recv_int()
  print ('\nreceived g1_a2')

  b2 = randrange(2, p)
  g1_b2 = pow(g1, b2, p)
  send(g1_b2)
  print ('\nsent g1_b2:', recv())

  g1_a3 = recv_int()
  print ('\nreceived g1_a3')

  b3 = randrange(2, p)
  g1_b3 = pow(g1, b3, p)
  send(g1_b3)
  print ('\nsent g1_b3:', recv())

  P_a = recv_int()
  print ('\nreceived P_a')

  b = randrange(2, p)
  g3 = pow(g1_a3, b3, p)

  P_b = pow(g3, b, p)
  send(P_b)
  print ('\nsent P_b:', recv())

  Q_a = recv_int()
  print ('\nreceived Q_a')
  g2 = pow(g1_a2, b2, p)

  y = int(sha1(DH_key + passphrase).hexdigest(), 16)

  Q_b = pow(g1, b, p) * pow(g2, y, p)
  send(Q_b)
  print ('\nsent Q_b:', recv())

  R_a = recv_int()
  print ('\nreceived R_a')

  Q_b_inv = modinv(Q_b, p)

  R_b = pow(Q_a * Q_b_inv, b3, p)
  send(R_b)
  print ('\nsent R_b:', recv())

  print ('\nAuthenticated', recv())

  R_ab = pow(R_a, b3, p)
  P_b_inv = modinv(P_b, p)
  print('Verification', R_ab == P_a * P_b_inv % p)

  msg = I2OSP(0, len(DH_key) - len(msg) // 2) + unhexlify(msg)

  enc_msg = base256([a ^ b for a, b in zip(msg, DH_key)])
  send(enc_msg)
  return recv()

if __name__ == '__main__':
  if not len(argv) == 2: raise Exception("Please input message in args")
  msg = argv[1]
  g = g1 = 2
  passphrase = b'eitn41 <3'
  p = int("FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF", 16)
  encr_msg = otr_smp(p, g, g1, msg, passphrase)
  print(encr_msg)

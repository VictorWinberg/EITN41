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

def read_buffer():
  lines = []
  while True:
    try:
      lines.append(input())
    except EOFError:
      break
  return lines

def getasn1value(line):
  return int(line.split('INTEGER')[1].strip()[1:], 16)

if __name__ == "__main__":
  print('2. generate asn1 file in python')
  
  lines = read_buffer()
  e, p, q = [ getasn1value(line) for line in [lines[3], lines[5], lines[6]] ]

  n = p * q
  d = modinv(e, totient(p, q))
  e1 = d % (p - 1)
  e2 = d % (q - 1)
  coeff = modinv(q, p)

  with open('input/b1/asn.cnf', 'r') as f:
    content = f.read()

  output = content.format(0, n, e, d, p, q, e1, e2, coeff)

  fh = open('output/asn.cnf', 'w')
  fh.write(output)
  fh.close()

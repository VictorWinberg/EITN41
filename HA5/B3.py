from binascii import unhexlify
from base64 import b64encode

def hex2(x):
  return '{}{:x}'.format('0' * (len(hex(x)) % 2), x)

def der_encode(x):
  hex_x = hex2(x)
  if int(hex_x[0], 16) >= 0b1000:
    # signed representation of two’s complement
    hex_x = '00' + hex_x

  l = hex2(len(hex_x))
  if len(hex_x) >= 0b10000000:
    # Long definite form
    l_encode = '8' + str(len(l) // 2) + l
  else:
    # Short definite form
    l_encode = '{:02x}'.format(len(hex_x) // 2)
  # Tag 0x02 INTEGER
  der = '02{}{}'.format(l_encode, hex_x)
  return der

def der_sequence(L):
  seq = ''.join(L)
  # Tag 0x30 SEQUENCE
  return unhexlify('30' + hex2(len(seq) // 2) + seq)

if __name__ == "__main__":
  X = [
    0,
    6610823582647678679,
    65537,
    3920879998437651233,
    2530368937,
    2612592767,
    2013885953,
    1498103913,
    1490876340
  ]

  DER_correct = [
    '020100',
    '02085bbe5d05d47d76d7',
    '0203010001',
    '02083669c395b9cf7321',
    '02050096d25da9',
    '0205009bb9007f',
    '020478097601',
    '0204594b4069',
    '020458dcf7b4'
  ]

  DER_calc = [ der_encode(x) for x in X ]
  [ print(DER_calc[i], DER_calc[i] == DER_correct[i]) for i in range(len(X)) ]

  rsa_seq = der_sequence(DER_calc)

  print(b64encode(rsa_seq).decode('utf-8'))

  # x = 161863091426469985001358176493540241719547661391527305133576978132107887717901972545655469921112454527920502763568908799229786534949082469136818503316047702610019730504769581772016806386178260077157969035841180863069299401978140025225333279044855057641079117234814239380100022886557142183337228046784055073741

  # print(der_encode(x))

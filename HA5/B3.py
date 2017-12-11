def der_encode(x):
  hex_x = '{}{:x}'.format('0' * (len(hex(x)) % 2), x)
  if int(hex_x[0], 16) >= 0b1000:
    hex_x = '00' + hex_x
  der = '02{:02x}{}'.format(len(hex_x) // 2, hex_x)
  return der

if __name__ == "__main__":
  X = [
    6610823582647678679,
    65537,
    3920879998437651233,
    2530368937,
    2612592767,
    2013885953,
    1498103913,
    1490876340
  ]

  DER = [
    '02085bbe5d05d47d76d7',
    '0203010001',
    '02083669c395b9cf7321',
    '02050096d25da9',
    '0205009bb9007f',
    '020478097601',
    '0204594b4069',
    '020458dcf7b4'
  ]

  [ print(der_encode(x), der_encode(x) == DER[i]) for i, x in enumerate(X) ]

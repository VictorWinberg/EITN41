import requests

def sort(chars, size=3):
  top = sorted(chars, key=lambda x: -x[1])[:size]
  return [ x for x, y in top ]

def most_common(L):
  return max(set(L), key=L.count)

requests.packages.urllib3.disable_warnings()
hex_string = '0123456789abcdef'

def chrcmp_hack(name, grade):
  url = 'https://eitn41.eit.lth.se:3119/ha4/addgrade.php'
  params = {'name': name, 'grade': grade, 'signature': ''}
  print(params)

  signature = [''] * 20

  for i in range(len(signature)):
    sig_chars = []
    for RETRY in range(15):
      chars = []
      for j in range(len(hex_string)):
        params['signature'] = ''.join(signature[:i]) + hex_string[j]

        r = requests.get(url, params, verify=False)
        t = r.elapsed.total_seconds()

        chars.append((hex_string[j], t))

      sig_chars.extend(sort(chars))

    signature[i] = most_common(sig_chars)
    print(''.join(signature))
  
  return ''.join(signature)

if __name__ == '__main__':
  print('6823ea50b133c58cba36')
  sign = chrcmp_hack(input('Name: '), int(input('Grade: ')))
  print(sign)

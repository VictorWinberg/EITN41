from sys import argv

def encode(word):
  res = ''
  for char in word:
    res += chr(ord(char) + inc)
  return res

if(len(argv) > 2):
  inc = int(argv[1])
  print(encode(argv[2]))
elif(len(argv) > 1):
  inc = int(argv[1])
  while True:
    word = input('> ')
    print(encode(word))
else:
  print('Usage: py string_encoder.py inc [arg]')
  print('   inc: set increment amount, e.g: 1 or -1')
  print('   arg: [optional]')

def bin_to_int(x):
  return int(x, 2)

def bin_to_hex(x):
  return hex(bin_to_int(x))

def hex_to_bin(x):
  return '{0:08b}'.format(int(x, 16))

def map_split(f, x):
  return list(map(f, x.split(' ')))

# Debugging
import pdb
debug = input("Debug (y/N)? ")

if(debug == 'y' or debug == 'yes'):
  pdb.set_trace()

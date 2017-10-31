import binascii
import hashlib
import unittest

def byte_to_int(x):
    x_in_int = int.from_bytes(x, byteorder='big')
    print('bytes ' + byte_to_hex(x) + ' to int: ' + str(x_in_int))
    return x_in_int

def byte_to_hex(x):
    return binascii.hexlify(x).decode('utf-8')

def byte_to_hash(x):
    x_in_hash = hashlib.sha1(x).digest()
    print('bytes ' + byte_to_hex(x) + ' to SHA1 hash: ' + byte_to_hex(x_in_hash))
    return x_in_hash

def int_to_byte(x):
    x_in_byte = (x).to_bytes(4, byteorder='big')
    print('int ' + str(x) + ' to 4-byte (big-endian): ' + byte_to_hex(x_in_byte))
    return x_in_byte

def hex_to_byte(x):
    x_in_byte = binascii.unhexlify(x)
    return x_in_byte

# Debugging
import pdb
debug = input("Debug (y/N)? ")

if(debug == 'y' or debug == 'yes' or debug == 'Yes'):
    pdb.set_trace()

# Test Cases
def test_int_to_byte():
    res_bytes = int_to_byte(500)
    ans_bytes = binascii.unhexlify('000001f4')
    assert res_bytes == ans_bytes

def test_int_to_hash():
    res_hash = byte_to_hex(byte_to_hash(int_to_byte(500)))
    ans_hash = 'c6c5da207269aa4a59743ded27105b13bc8dd384'
    assert res_hash == ans_hash

def test_str_to_int():
    res_int = byte_to_int(hex_to_byte('fedcba9876543210'))
    ans_int = 18364758544493064720
    assert res_int == ans_int

def test_str_to_hash():
    res_hash = byte_to_int(byte_to_hash(hex_to_byte('fedcba9876543210')))
    ans_hash = 946229717077375328329532411653585908948565005770
    assert res_hash == ans_hash

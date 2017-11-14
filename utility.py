import binascii
import hashlib
import unittest

def bytes_to_int(x, byteorder='big'):
    return int.from_bytes(x, byteorder)

def bytes_to_hex(x):
    return binascii.hexlify(x).decode('utf-8')

def bytes_to_hash(x):
    return hashlib.sha1(x).digest()

def int_to_bytes(x, length=4, byteorder='big'):
    return (x).to_bytes(length, byteorder)

def int_to_hex(x):
    return hex(x)

def hex_to_bytes(x):
    return binascii.unhexlify(x)

def hex_to_int(x):
    return int(x, 16)

# Test Cases
def test_int_to_bytes():
    res_bytes = int_to_bytes(500)
    ans_bytes = binascii.unhexlify('000001f4')
    assert res_bytes == ans_bytes

def test_int_to_hash():
    res_hash = bytes_to_hex(bytes_to_hash(int_to_bytes(500)))
    ans_hash = 'c6c5da207269aa4a59743ded27105b13bc8dd384'
    assert res_hash == ans_hash

def test_str_to_int():
    res_int = bytes_to_int(hex_to_bytes('fedcba9876543210'))
    ans_int = 18364758544493064720
    assert res_int == ans_int

def test_str_to_hash():
    res_hash = bytes_to_int(bytes_to_hash(hex_to_bytes('fedcba9876543210')))
    ans_hash = 946229717077375328329532411653585908948565005770
    assert res_hash == ans_hash

if __name__ == "__main__":
    # Debugging
    import pdb
    debug = input("Debug (y/N)? ")

    if(debug == 'y' or debug == 'yes'):
        pdb.set_trace()

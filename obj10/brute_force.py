#!/usr/bin/python3

import datetime
from des import DesKey

# the first 8 bytes of our cipher text to try decrypting
ciphertext = b"\x5d\xbd\xce\xdc\x49\x4a\x74\x43"

# define the period which we know the crypto key was generated
epoch = datetime.datetime(1970,1,1)
start_time = int((datetime.datetime(2019,12,6,19) - epoch).total_seconds())
finish_time = int((datetime.datetime(2019,12,6,21) - epoch).total_seconds())

# loop through each second of that period
for test_time in range(start_time, finish_time):
    # seed prng and generate key
    prng_state = test_time
    key = bytearray()
    for key_byte in range(8):
        prng_state = (prng_state * 0x343fd) + 0x269ec3
        key.append(((prng_state >> 0x10) & 0x7fff) & 0xff)

    # attempt decrypt
    des_key = DesKey(key)
    plaintext = des_key.decrypt(ciphertext)

    # print details of the seed, key and decrypted ciphertext
    print("T=" + str(test_time) + " Key=" + ''.join(format(x, '02x') for x in key) + " Plaintext=" + ''.join(format(x, '02x') for x in plaintext))


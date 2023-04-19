#!/usr/bin/env python3 
import unittest


def encode(rawbuf, delim=0):
    return rawbuf

def decode(cobsbuf, delim=0):
    return cobsbuf

"""All tests will fail until implementation is done."""
class testCobs(unittest.TestCase):
    goodShortCases = [
       ( bytes.fromhex("00 aa 00"), bytes.fromhex("01 02 aa 00") ),
       ( bytes.fromhex("aa bb 00"), bytes.fromhex("03 aa bb 00") )
    ]

    def testShort(self):
        for (plainbuf, cobsbuf) in self.goodShortCases:
            self.assertEqual(encode(plainbuf), cobsbuf)
            self.assertEqual(decode(cobsbuf), plainbuf)

if __name__ == '__main__':
    print("try: python3 -m unittest cobs.py")

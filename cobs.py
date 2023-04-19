#!/usr/bin/env python3 
import unittest


def encode(rawbuf, delim=0):
    return rawbuf

def decode(cobsbuf, delim=0):
    return cobsbuf

"""All tests will fail until implementation is done."""
class testCobs(unittest.TestCase):
    staticCases = [
       ( bytes.fromhex("00 aa 00"), bytes.fromhex("01 02 aa 00") ),
       ( bytes.fromhex("aa bb 00"), bytes.fromhex("03 aa bb 00") )
    ]

    def testStatic(self):
        for (plainbuf, cobsbuf) in self.staticCases:
            self.assertEqual(encode(plainbuf), decode(cobsbuf))

if __name__ == '__main__':
    print("This is hell\n")

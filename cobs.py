#!/usr/bin/env python3 
import unittest

""" COBS Encoder and Decoder

Consistent Overhead Byte Stuffing is a way to frame binary serial data.  
The advantage of COBS is that the worst use case adds ceiling(n/254)+1 bytes
to the transmitted data.  By contrast, some other framing (like HDLC) can
double the data size in their worst-case scenarios.

Paper:     http://www.stuartcheshire.org/papers/COBSforToN.pdf
Wikipedia: https://en.wikipedia.org/wiki/Consistent_Overhead_Byte_Stuffing

For examples, see 'goodCasesZero' in the unit test.

The first implementations will be intentionally simple.  Once they're working,
I want to test the effect of using different techniques on both CPU and memory 
overhead.  The overall goal should be to achieve reasonable performce with 
a high degree of consistency.
"""

"""Encode the given bytes-like object with COBS

    Adds a terminating byte.
"""
def encode(rawbuf, delim=0):
    outbuf = bytearray()
    maxblock = 254
    delimBytes = delim.to_bytes(1, signed=False)

    if len(rawbuf) > 0:
        blocks = rawbuf.split(delimBytes)
        for oneBlock in blocks:
            pointer = 0
            while pointer + maxblock <= len(oneBlock):
                outbuf.append(255)
                outbuf.extend(oneBlock[pointer:pointer+maxblock])
                pointer += maxblock
            outbuf.append(len(oneBlock)-pointer+1)
            outbuf.extend(oneBlock[pointer:])

    outbuf.append(delim)
    return outbuf

def decode(cobsbuf, delim=0):
    return cobsbuf

"""All tests will fail until implementation is done."""
class testCobs(unittest.TestCase):
    goodCasesZero = [
        ( bytes.fromhex(""), bytes.fromhex("00") ),
        ( bytes.fromhex("00"), bytes.fromhex("01 01 00") ),
        ( bytes.fromhex("00 00"), bytes.fromhex("01 01 01 00") ),
        ( bytes.fromhex("00 11 00"), bytes.fromhex("01 02 11 01 00") ),
        ( bytes.fromhex("11 22 00 33"), bytes.fromhex("03 11 22 02 33 00") ),
        ( bytes.fromhex("11 22 33 44"), bytes.fromhex("05 11 22 33 44 00") ),
        ( bytes.fromhex("11 00 00 00"), bytes.fromhex("02 11 01 01 01 00") ),
    ]

    def testShort(self):
        for (plainbuf, cobsbuf) in self.goodCasesZero:
            self.assertEqual(encode(plainbuf), cobsbuf)
            #self.assertEqual(decode(cobsbuf), plainbuf)
    
    longCases = [
        ( bytes.fromhex("""0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 
                         0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 
                         0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 
                         0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 
                         0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF"""),
          bytes.fromhex("""FF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 
                         0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 
                         0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 
                         0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789AB
                         43 CDEF 
                         0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 
                         00""")
        )
    ]
    def testLong(self):
        for (plainbuf, cobsbuf) in self.longCases:
            self.assertEqual(encode(plainbuf), cobsbuf)
            #self.assertEqual(decode(cobsbuf), plainbuf)


if __name__ == '__main__':
    print("try: python3 -m unittest cobs.py")

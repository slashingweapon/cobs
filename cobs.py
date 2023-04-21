#!/usr/bin/env python3 
import unittest

""" COBS Encoder and Decoder

Consistent Overhead Byte Stuffing is a way to frame binary serial data.  
The advantage of COBS is that the worst use case adds floor(n/254) bytes
to the transmitted data.  By contrast, some other framing (like HDLC) have
substatially worse worst-case scenarios.

Paper:     http://www.stuartcheshire.org/papers/COBSforToN.pdf
Wikipedia: https://en.wikipedia.org/wiki/Consistent_Overhead_Byte_Stuffing

For examples, see 'goodCasesZero' in the unit test.

The first implementations will be intentionally simple.  Once they're working,
I want to test the effect of using different techniques on both CPU and memory 
overhead.  The overall goal should be to achieve reasonable performce with 
a high degree of consistency.
"""

""" Encode the given bytes-like object with COBS

    Does not add terminating byte.
    returns a bytearray object
"""
def encode(rawbuf, delim=0):
    outbuf = bytearray()
    maxblock = 254
    delimBytes = delim.to_bytes(1, signed=False)

    if len(rawbuf) > 0:
        blocks = rawbuf.split(delimBytes)
        for oneBlock in blocks:
            pos = 0
            while pos + maxblock <= len(oneBlock):
                outbuf.append(255)
                outbuf.extend(oneBlock[pos:pos+maxblock])
                pos += maxblock
            if (pos == 0) or (pos < len(oneBlock)):
                outbuf.append(len(oneBlock)-pos+1)
                outbuf.extend(oneBlock[pos:])

    return outbuf

""" Decode a COBS frame to the original data.

    Decodes the COBS data until until the end of the input is reached, or
    the delimiter is encountered.  If the delimiter is present in the input
    then it will be consumed (and counted as such), but it will not be present
    in the output.

    returns (consumedByteCount, outputArray)
    raises ValueError if the last value is malformed (eg: there aren't enough bytes at the end)
"""
def decode(cobsbuf, delim=0):
    outbuf = bytearray()
    firstBlock = True
    pos = 0

    while pos < len(cobsbuf):
        # Add a delimiter between blocks
        if not firstBlock:
            outbuf.append(delim)
        else:
            firstBlock = False
        blockSize = cobsbuf[pos]

        # Carve out the next slice and append it to the output,
        # but check a few things first.

        # Check for end of frame
        if blockSize == delim:
            pos += 1
            break
        # Check for invalid block size.  This can happen when the delimiter value is not 0
        # Check that our next block isn't bigger than the remaining buffer
        elif (blockSize == 0) or (pos + blockSize - 1 >= len(cobsbuf)):
            raise ValueError("Invalid COBS block size")
        # Make our slice, and add it nice
        else:
            block = cobsbuf[pos:pos+blockSize-1]
            if block.find(delim) == -1:
                outbuf.extend(block)
                pos += blockSize
            else:
                raise ValueError("Delimiter found in COBS block")
    
    return (pos, cobsbuf)

"""All tests will fail until implementation is done."""
class testCobs(unittest.TestCase):
    goodCasesZero = [
        ( "empty",              bytes.fromhex(""), bytes.fromhex("") ),
        ( "a zero",             bytes.fromhex("00"), bytes.fromhex("01 01") ),
        ( "two zeroes",         bytes.fromhex("00 00"), bytes.fromhex("01 01 01") ),
        ( "sandwich zeroes",    bytes.fromhex("00 11 00"), bytes.fromhex("01 02 11 01") ),
        ( "embedded zero",      bytes.fromhex("11 22 00 33"), bytes.fromhex("03 11 22 02 33") ),
        ( "no zeroes",          bytes.fromhex("11 22 33 44"), bytes.fromhex("05 11 22 33 44") ),
        ( "trailing zeroes",    bytes.fromhex("11 00 00 00"), bytes.fromhex("02 11 01 01 01") ),
    ]

    def testShort(self):
        for (name, plainbuf, cobsbuf) in self.goodCasesZero:
            with self.subTest(name=name):
                self.assertEqual(encode(plainbuf), cobsbuf)
                (bytesEaten, decodedBytes) = decode(cobsbuf)
                self.assertEqual(bytesEaten, len(cobsbuf))
                self.assertEqual(decodedBytes, cobsbuf)
    
    longCases = [
        ( "long 320",
          bytes.fromhex("""0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 
                         0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 
                         0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 
                         0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 
                         0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF """),
          bytes.fromhex("""FF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 
                         0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 
                         0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 
                         0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789AB
                         43 CDEF 
                         0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF """),
        ),
        ( "long 254",
          bytes(b"""This is a string that is sixty four bytes long and is useful...
This is a string that is sixty four bytes long and is useful...
This is a string that is sixty four bytes long and is useful...
This is a string that is sixty four bytes long and is useful.."""),
          bytes(b"""\xffThis is a string that is sixty four bytes long and is useful...
This is a string that is sixty four bytes long and is useful...
This is a string that is sixty four bytes long and is useful...
This is a string that is sixty four bytes long and is useful.."""),
        ),
    ]

    def testLong(self):
        for (name, plainbuf, cobsbuf) in self.longCases:
            with self.subTest(name=name):
                # The unused variables here are intentional, for use with
                # the --local flag.
                plainLen = len(plainbuf)
                cobsLen = len(cobsbuf)
                encodedBytes = encode(plainbuf)
                encodedLen = len(encodedBytes)
                self.assertEqual(encodedBytes, cobsbuf)
                (decodedLen, decodedBytes) = decode(cobsbuf)
                self.assertEqual(decodedLen, len(cobsbuf))
                self.assertEqual(decodedBytes, cobsbuf)

    errorCases = [
        ("short block", bytes.fromhex("0A 11223344 55667788")),
        ("delim in block", bytes.fromhex("09 01020304 00060708")),
    ]
    def testDecodeErrors(self):
        for (name, cobsbuf) in self.errorCases:
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    (decodedLen, decodedBytes) = decode(cobsbuf)

if __name__ == '__main__':
    print("try: python3 -m unittest cobs.py")

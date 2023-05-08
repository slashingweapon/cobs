#!/usr/bin/env python3

from cobs import codec
import unittest

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
                self.assertEqual(codec.encode(plainbuf), cobsbuf)
                (bytesEaten, decodedBytes) = codec.decode(cobsbuf)
                self.assertEqual(bytesEaten, len(cobsbuf))
                self.assertEqual(decodedBytes, plainbuf)

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
                encodedBytes = codec.encode(plainbuf)
                encodedLen = len(encodedBytes)
                self.assertEqual(encodedBytes, cobsbuf)
                (decodedLen, decodedBytes) = codec.decode(cobsbuf)
                self.assertEqual(decodedLen, cobsLen)
                self.assertEqual(decodedBytes, plainbuf)

    errorCases = [
        ("short block", bytes.fromhex("0A 11223344 55667788")),
        ("delim in block", bytes.fromhex("09 01020304 00060708")),
    ]
    def testDecodeErrors(self):
        for (name, cobsbuf) in self.errorCases:
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    (decodedLen, decodedBytes) = codec.decode(cobsbuf)

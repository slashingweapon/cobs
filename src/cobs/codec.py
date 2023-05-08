#!/usr/bin/env python3 

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
        # Add a delimiter between blocks, except on the first block
        # and when a max-sized block is encountered.
        if not firstBlock:
            outbuf.append(delim)
        else:
            firstBlock = False
        blockSize = cobsbuf[pos]

        # Carve out the next slice and append it to the output,
        # but check a few things first.

        # Check for invalid block size.  This can happen when the delimiter value is not 0
        # Check that our next block isn't bigger than the remaining buffer
        if (blockSize == 0) or (pos + blockSize - 1 >= len(cobsbuf)):
            raise ValueError("Invalid COBS block size")
        # Make our slice, and add it nice
        else:
            block = cobsbuf[pos+1:pos+blockSize]
            if block.find(delim) == -1:
                outbuf.extend(block)
                pos += blockSize
                if blockSize == 255:
                    firstBlock = True # suppress the delimiter when max-sized block is encountered
            else:
                raise ValueError("Delimiter found in COBS block")
    
    return (pos, outbuf)


# COBS -- Consistent Overhead Byte Stuffing

A module to support COBS framing.

## Background

A common task for embedded programmers is reading data from a serial connection.
SPI and UART are the two interfaces that come immediately to mind.  If the data
is text, then it is easy to separate messages by line or some other value.  (Think
NEMA sentences that come out of GPS chips).  If the data is binary and there are
no reserved values, then you need some kind of message framing.

Consistent Overhead Byte Stuffing is a way to frame binary serial data.  
The advantage of COBS is that the worst use case adds floor(n/254) bytes
to the transmitted data.  By contrast, some other framing (like HDLC) have
substatially worse worst-case scenarios.

Paper:     http://www.stuartcheshire.org/papers/COBSforToN.pdf
Wikipedia: https://en.wikipedia.org/wiki/Consistent_Overhead_Byte_Stuffing

For example data, see `tests/test_cobs.py` in the tests folder.

### Implementation Plan

The first implementations is intentionally simple.  Next,
I want to test the effect of using different techniques on both CPU and memory 
overhead.  The overall goal is to achieve reasonable performce with 
a high degree of consistency.

After I have a good handle on the performance issues (and have reliable tooling
and metrics) then I'll flesh out the full suite of goodies to make COBS a regular
Python codec and protocol, so it is usable with network streams etc..

## Installation

## Uses

## Testing

To run the unit test from the repo root:

    PYTHONPATH=`pwd`/src python3 -m unittest tests/test_cobs.py

This should allow the unittest to find and load the cobs module without issue.

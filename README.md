# COBS -- Consistent Overhead Byte Stuffing

A module to support COBS framing.

## Background

A common task for embedded programmers is reading data from a serial connection.
SPI and UART are the two interfaces that come immediately to mind.  If the data
is text, then it is easy to separate messages by line or some other value.  (Think
NEMA sentences that come out of GPS chips.)  However, if the data is binary and there are
no reserved values, then you need some kind of message framing.

Consistent Overhead Byte Stuffing is a way to frame binary serial data. The
advantage of COBS is that the worst use case adds floor(n/254) bytes
to the transmitted data.  By contrast, some other framing (like HDLC) have
substatially worse worst-case scenarios.

Original Paper: http://www.stuartcheshire.org/papers/COBSforToN.pdf

Wikipedia: https://en.wikipedia.org/wiki/Consistent_Overhead_Byte_Stuffing

For example data, see `tests/test_cobs.py` in the tests folder.

### Implementation Plan

The first implementation is intentionally simple and almost certainly inefficient.
Next, I want to test the effect of using different techniques on both CPU and memory 
overhead.  That means gaining reliable tooling and metrics.  The overall goal is to
achieve reasonable performce with a high degree of consistency.

After I have a good handle on the performance issues, I'll flesh out the full suite
of goodies to make COBS a regular Python codec and protocol, so it is usable with 
network streams, asyncio, etc..

## Installation

## Uses

## Testing

To run the unit test from the repo root:

    PYTHONPATH=`pwd`/src python3 -m unittest tests/test_cobs.py

This should allow the unittest to find and load the cobs module without issue.

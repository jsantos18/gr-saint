#!/usr/bin/env python

# This is a redesign of a qam block already in gnuradio but for odd points
# which is not a even poly of 4 which is not made yet. Since odd QAM is a
# cross qam it is not gray coded nor does it have differential

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from math import pi, sqrt, log

from gnuradio import gr
from gnuradio.digital.generic_mod_demod import generic_mod, generic_demod
from gnuradio.digital.generic_mod_demod import shared_mod_args, shared_demod_args
from gnuradio.digital.utils.gray_code import gray_code
from gnuradio.digital.utils import mod_codes
from gnuradio.digital import modulation_utils
from gnuradio.digital import digital_swig as digital

# Default Number of points in qam 32 constellation
_def_constellation_points = 32

def is_power_of_two(x):
    v = log(x) / log(2)
    return int(v) == v

def get_bit(x, n):
    ''' Get the n'th bit of integer x (from little end). '''
    return (x&(0x01 << n)) >> n

def get_bits(x, n, k):
    """ Get the k bits of integer x starting at bit n(from little end)."""
    # Remove the n smallest bits
    v = x >> n
    # Remove all bits bigger than n+k-1
    return v % pow(2, k)
    
def make_constellation(m):
    """
    Create a constellation with m possible symbols where m must be a power
    of 2.

    Points are laid out in a cross grid.

    Bits re
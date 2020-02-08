#!/usr/bin/env python

# This is a redesign of a qam block already in gnuradio but for odd points
# which is not a even poly of 4 which is not made yet. Since odd QAM is a
# cross qam it has a different type of gray coding defined here
# http://www.ieee802.org/3/bn/public/nov13/prodan_3bn_02_1113.pdf

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
import numpy as np

# Default Number of points in qam 32 constellation
_def_constellation_points = 32
# Default Gray Coding
_def_mod_code = mod_codes.GRAY_CODE


def is_odd_power_of_two(x):
    v = log(x) / log(2)
    return int(v) == v and v % 2 == 1


def get_bit(x, n):
    """ Get the n'th bit of integer x (from little end). """
    return (x & (0x01 << n)) >> n


def get_bits(x, n, k):
    """ Get the k bits of integer x starting at bit n(from little end)."""
    # Remove the n smallest bits
    v = x >> n
    # Remove all bits bigger than n+k-1
    return v % pow(2, k)


def G(bits=[0b0]):
    """ Does the One Dimensional Grey Code Mapping """
    k = len(bits)
    if k == 1:
        if bits[0] == 0:
            return 1
        else:
            return -1
    else:
        coeff = 1 - (2 * bits[0])
        poly = pow(2, k - 1)
        lower_G = G(bits[1:])
        Gk = coeff * (poly + lower_G)
        return Gk


def rectG(a=[0], b=[0]):
    I = G(a)
    Q = G(b)
    return I, Q


def sign(x):
    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return 1


def convert_to_binary(x: int, k: int):
    int_array = np.array([x])
    bin_array = ((int_array[:None] & (1 << np.arange(int(k)))) > 0).astype(int)
    return bin_array.tolist()


def make_constellation(m):
    """
    Create a constellation with m possible symbols where m must be a power
    of 2.

    Points are laid out in a cross grid.
    """
    if not isinstance(m, int) or not is_odd_power_of_two(m) and m > 1:
        raise ValueError("m must be an odd power of 2 integer.")
    # Each symbol holds k bits.
    k = int(log(m) / log(2))
    n = int(k / 2) + 1
    mn = k - n
    s = int(pow(2, mn - 1))

    # Determining how the constellation map should be build
    rect_map = []
    const_map = [0 + 0j] * m
    if k == 1:
        const_map.append(complex(1, 0))
        const_map.append(complex(-1, 0))
    elif k == 3:
        # Do rectangular constellation mapping first
        for i in range(2 * pow(2, s)):
            i_bin = convert_to_binary(i, s + 1)
            for j in range(pow(2, s)):
                j_bin = convert_to_binary(j, s)
                rect_map.append((i_bin, j_bin))

        # Make Complex Constellation using cross gray coding
        for x, y in rect_map:
            Irct, Qrct = rectG(x, y)
            z = np.packbits(np.append(y, x[::-1]), bitorder='little')[0]
            if Irct < 3:
                const_map[z] = complex(Irct, Qrct)
            else:
                Icr = -sign(Irct) * (4 - abs(Irct))
                Qcr = sign(Qrct) * (abs(Qrct) + 2)
                const_map[z] = complex(Icr, Qcr)
    else:
        # Do rectangular constellation mapping first
        for i in range(pow(2, n)):
            i_bin = convert_to_binary(i, n)
            for j in range(pow(2, mn)):
                j_bin = convert_to_binary(j, mn)
                rect_map.append((i_bin, j_bin))

        # Make Numpy Complex Constellation using cross gray coding
        for x, y in rect_map:
            Irct, Qrct = rectG(x, y)
            xy = x + y
            z = int("".join(str(w) for w in xy), 2)
            if abs(Irct) < (3 * s):
                const_map[z] = complex(Irct, Qrct)
            elif abs(Qrct) > s:
                Icr = sign(Irct) * (abs(Irct) - (2 * s))
                Qcr = sign(Qrct) * ((4 * s) - abs(Qrct))
                const_map[z] = complex(Icr, Qcr)
            else:
                Icr = sign(Irct) * ((4 * s) - abs(Irct))
                Qcr = sign(Qrct) * (abs(Qrct) + (2 * s))
                const_map[z] = complex(Icr, Qcr)
    return const_map


def qam_constellation(constellation_points=_def_constellation_points):
    """
    Creates an Odd QAM constellation object
    """
    points = make_constellation(constellation_points)

    pre_diff_code = []
    k = int(log(constellation_points) / log(2))
    n = int(k / 2) + 1
    m = k - n
    wn = 2.0 / (n - 1)
    wm = 2.0 / (m - 1)
    constellation = digital.constellation_rect(points, pre_diff_code, 4, n, m, wn, wm)

    return constellation


def find_closet_point(p, qs):
    """
    Return in dex of the closest point in 'qs' to 'p'.
    """
    min_dist, min_i = None, None
    for i, q in enumerate(qs):
        dist = abs(q-p)
        if min_dist is None or dist < min_dist:
            min_dist = dist
            min_i = i
    return min_i


modulation_utils.add_type_1_constellation('qam_odd', qam_constellation)

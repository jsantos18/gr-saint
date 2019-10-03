#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Julian Santos
import math

def timeslot_distance(current, target, bitwidth):
    c_bits = int(math.pow(2, 2 * bitwidth)) >> current
    t_bits = int(math.pow(2, bitwidth) + 1) * target
    if (c_bits & t_bits): return 0
    elif (c_bits >> 1 & t_bits): return 1
    elif (c_bits >> 2 & t_bits): return 2
    elif (c_bits >> 3 & t_bits): return 3

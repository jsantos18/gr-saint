#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Julian Santos

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from fast_autocorrelator import fast_autocorrelator_c, fast_autocorrelator_f
import numpy
import struct
import math

class qa_fast_autocorrelator(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_t(self):
        # set up fg
        src_data = numpy.zeros(1024 * 4)
        src = blocks.vector_source_f(src_data)
        fac = fast_autocorrelator_f(1, 256, 10)
        snk = blocks.vector_sink_f()
        self.tb.connect(src, fac)
        self.tb.connect(fac, snk)
        self.tb.run()
        # check data


if __name__ == '__main__':
    gr_unittest.run(qa_fast_autocorrelator)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Julian Santos

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from fast_autocorrelator import fast_autocorrelator

class qa_fast_autocorrelator(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_t(self):
        # set up fg
        self.tb.run()
        # check data


if __name__ == '__main__':
    gr_unittest.run(qa_fast_autocorrelator)

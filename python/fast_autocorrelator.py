#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Julian Santos

from gnuradio import gr, blocks, filter, fft
import math

class fast_autocorrelator_c(gr.hier_block2):
    """
    A Python Hierarchy Block for Fast Autocorrelation Block. 
    GNU Radio 3.8.0.0 Block
    """
    def __init__(self, sample_rate, fac_size, fac_rate):
        gr.hier_block2.__init__(self,
            "fast_autocorrelator_c",
            gr.io_signature(1, 1, gr.sizeof_gr_complex),
            gr.io_signature(1, 1, gr.sizeof_float)
        )
        # Parameters
        self.sample_rate = sample_rate
        self.fac_size = fac_size
        self.fac_rate = fac_rate
        self.window = ()

        # Block Objects For Complex Fast Autocorrelator
        self.stream_to_vector = blocks.stream_to_vector(gr.sizeof_gr_complex, fac_size)
        self.keep_one_in_n = blocks.keep_one_in_n(gr.sizeof_gr_complex * fac_size, max(1, int(sample_rate/fac_size/fac_rate)))
        self.fac_fft = fft.fft_vfc(fac_size, True, self.window)
        self.complex_to_mag = blocks.complex_to_mag(fac_size)
        self.fac_complex_to_mag = blocks.complex_to_mag(fac_size)
        self.nlog10_ff = blocks.nlog10_ff(20, fac_size, -20 * math.log10(fac_size))
        self.single_pole_iir_filter_ff = filter.single_pole_iir_filter_ff(1.0, fac_size)
        self.fft_vcc = fft.fft_vcc(fac_size, True, self.window)
        self.vector_to_stream = blocks.vector_to_stream(gr.sizeof_float, self.fac_size)

        # Connections for Auto Correlator
        self.connect(self, self.stream_to_vector, self.keep_one_in_n, self.fft_vcc, self.complex_to_mag,
                        self.fac_fft, self.fac_complex_to_mag, self.single_pole_iir_filter_ff,
                        self.nlog10_ff, self.vector_to_stream, self)

class fast_autocorrelator_f(gr.hier_block2):
    """
    A Python Hierarchy Block for Fast Autocorrelation Block. 
    GNU Radio 3.8.0.0 Block
    """
    def __init__(self, sample_rate, fac_size, fac_rate):
        gr.hier_block2.__init__(self,
            "fast_autocorrelator_c",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(1, 1, gr.sizeof_float)
        )
        # Parameters
        self.sample_rate = sample_rate
        self.fac_size = fac_size
        self.fac_rate = fac_rate
        self.window = ()

        # Block Objects For Float Fast Autocorrelator
        self.stream_to_vector = blocks.stream_to_vector(gr.sizeof_float, fac_size)
        self.keep_one_in_n = blocks.keep_one_in_n(gr.sizeof_float * fac_size, max(1, int(sample_rate/fac_size/fac_rate)))
        self.fac_fft = fft.fft_vfc(fac_size, True, self.window)
        self.complex_to_mag = blocks.complex_to_mag(fac_size)
        self.fac_complex_to_mag = blocks.complex_to_mag(fac_size)
        self.nlog10_ff = blocks.nlog10_ff(20, fac_size, -20 * math.log10(fac_size))
        self.single_pole_iir_filter_ff = filter.single_pole_iir_filter_ff(1, fac_size)
        self.fft_vfc = fft.fft_vfc(fac_size, True, self.window)
        self.vector_to_stream = blocks.vector_to_stream(gr.sizeof_float, self.fac_size)

        # Connections for Auto Correlator
        self.connect(self, self.stream_to_vector, self.keep_one_in_n, self.fft_vfc, self.complex_to_mag,
                        self.fac_fft, self.fac_complex_to_mag, self.single_pole_iir_filter_ff,
                        self.nlog10_ff, self.vector_to_stream, self)
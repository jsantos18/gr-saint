/* -*- c++ -*- */

#define SAINT_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "saint_swig_doc.i"

%{
#include "saint/burst_message_multiplexer.h"
%}

%include "saint/burst_message_multiplexer.h"
GR_SWIG_BLOCK_MAGIC2(saint, burst_message_multiplexer);

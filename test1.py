#!/usr/bin/env python

"""
Simple example that doesn't require any C compiler, it just uses the ABI of the
shared object. Only need to put the functions you want to use in the cdef() call.

This is slower than the test2 counterpart with compiled code.
"""

from cffi import FFI

ffi = FFI()

lib = ffi.dlopen('/home/pklaus/phd/workrepos/trbnettools/trbnetd/libtrbnet.so')

# --- Describe the C signatures used lateron
ffi.cdef('''
int init_ports();

int trb_register_read(uint16_t trb_address,                             
                      uint16_t reg_address,                             
                      uint32_t* data,
                      unsigned int dsize);                                 

extern int trb_errno;

const char* trb_errorstr(int trberrno);

''')

# --- Connect to the trbnet daemon
status = lib.init_ports()
if status < 0:
    errno = lib.trb_errno
    errorstr = ffi.string(lib.trb_errorstr(errno)).decode('ascii')
    raise NameError('Error initialising ports.', errno, errorstr)

# --- Setting up the buffer given to library function calls
bufsize = 1024 # 32-bit words

# the buffer can be a numpy.array():
#import numpy as np
#buf = np.array([0]*bufsize, dtype=np.uint32)
# or a Python stdlib array.array():
import array
buf = array.array('I', [0]*bufsize)
assert buf.itemsize == 4 # otherwise try buf = array.array('L', [0]*bufsize)

# --- Casting the buffer to the right type required by the C library
buf_ffi = ffi.cast('uint32_t *', ffi.from_buffer(buf))

# --- Call the trb_register_read() function to query the broadcast address for register 0x0
status = lib.trb_register_read(0xffff, 0x0, buf_ffi, bufsize)
if status == -1:
    errno = lib.trb_errno
    errorstr = ffi.string(lib.trb_errorstr(errno)).decode('ascii')
    raise NameError('Error reading register', errno, errorstr)

# --- Read the response from the buffer
response_words = [(buf[i]) for i in range(status)]
for i in range(0, status, 2):
    print('TrbAddress', hex(response_words[i]), 'responded with:', hex(response_words[i+1]))

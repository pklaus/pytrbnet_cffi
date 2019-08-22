import os
from cffi import FFI
ffibuilder = FFI()


# ffibuilder.cdef() expects a single string declaring the C types, functions and
# globals needed to use the shared object. It must be in valid C syntax.
# eg.
#cdefinition = """
#    float pi_approx(int n);
#"""
cdefinition = ""
#for headerfile in ('trberror.h', 'trbnet.h'):
#    with open(os.path.join('../trbnettools/trbnetd', headerfile), 'r') as f:
#        cdefinition += f.read()
with open('trbnetheaders.cdef', 'r') as f:
    cdefinition += f.read()

ffibuilder.cdef(cdefinition)

# set_source() gives the name of the python extension module to
# produce, and some C source code as a string.  This C code needs
# to make the declarated functions, types and globals available,
# so it is often just the "#include".
ffibuilder.set_source("_trbnet_cffi",
"""
     #include "trbnet.h"   // the        C header of the library
     #include "trberror.h" // the errors C header of the library
""",
     libraries=['trbnet'],   # library name, for the linker
     library_dirs=['/home/pklaus/phd/workrepos/trbnettools/trbnetd/'],
     include_dirs=['/home/pklaus/phd/workrepos/trbnettools/trbnetd/'])

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)

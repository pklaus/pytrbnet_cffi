

.PHONY: all
all: build

.PHONY: build
build: _trbnet_cffi.cpython-37m-x86_64-linux-gnu.so
	
_trbnet_cffi.cpython-37m-x86_64-linux-gnu.so: trbnet_cffi_build.py trbnetheaders.cdef
	python3 trbnet_cffi_build.py

.PHONY: clean
clean:
	rm -f *.so
	rm -f *.o
	rm -f *.c

.PHONY: test
test: build
	./test.py

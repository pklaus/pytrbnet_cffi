
DAQOPSERVER ?= "not set - the tests might fail"
LD_LIBRARY_PATH ?= "not set - the tests might fail"
# should be something like /home/pklaus/phd/workrepos/trbnettools/trbnetd/

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
test: test0 test1 test2

.PHONY: test0
test0:
	@echo DAQOPSERVER = "$(DAQOPSERVER)"
	@echo LD_LIBRARY_PATH = "$(LD_LIBRARY_PATH)"

.PHONY: test1
test1:
	./test1.py

.PHONY: test2
test2: build
	./test2.py

# makefile to compile heartbeat module

heartbeat_python_lib: 
	gcc -shared -Wl,-soname,heartbeat_python_lib -o heartbeat_python_lib.so -fPIC heartbeat_python_lib.c
clean:
	-rm -f *lib.so
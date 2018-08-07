



#include <stdio.h>
#ifdef __cplusplus
extern "C" {
#endif
#include <xenstore.h>
#ifdef __cplusplus
}
#endif


// C function declarations
extern "C" {
	char * xenstore_read(struct xs_handle*  ,xs_transaction_t , const char*  , unsigned int * );
	void xenstore_write(struct xs_handle *, xs_transaction_t , const char *, const void *);
}


#include <cstdio>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <array>

int exec(const char* cmd) {
    array<char, 4> buffer;
    string result;
    shared_ptr<FILE> pipe(popen(cmd, "r"), pclose);
    if (!pipe) throw runtime_error("popen() failed!");
    while (!feof(pipe.get())) {
        if (fgets(buffer.data(), 4, pipe.get()) != nullptr)
            result += buffer.data();
    }
    return stoi(result);
}

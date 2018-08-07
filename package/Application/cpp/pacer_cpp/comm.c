
#include "comm.h"
// #include <string.h>
int xenstore_getDomid()
{

        int domid=0;
        FILE * stream;
        const int max_buffer = 256;
        char buffer[max_buffer];

        stream =popen("python3 -c \'from pyxs import Client;c=Client(xen_bus_path=\"/dev/xen/xenbus\");c.connect();print((c.read(\"domid\".encode())).decode());c.close()\'", "r");
        if (stream) {
        while (!feof(stream))
                if (fgets(buffer, max_buffer, stream) != NULL) sscanf(buffer, "%d", &domid);;
        pclose(stream);
        }
        return domid;

}

// helper for writing data to xenstore
void xenstore_write(struct xs_handle *xs, xs_transaction_t th, const char *path, const void *data)
{
	int er;
        th = xs_transaction_start(xs);
        er = xs_write(xs, th, path, data, strlen(data));
        xs_transaction_end(xs, th, false);
        return;
}
// helper for reading data from xenstore
char* xenstore_read(struct xs_handle* xs ,xs_transaction_t th, const char* path , unsigned int *len )
{
	char * buf;
	th = xs_transaction_start(xs);
	buf = xs_read(xs, th, path, len);
	xs_transaction_end(xs, th, false);
	return buf;
}

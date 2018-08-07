class Pacer
{
private:
  int domid;
    int domid;
    struct xs_handle* xs;
    xs_transaction_t th;
    char * base_path;
    heartbeat_t * heart;

public:
  Pacer();
  int getSum();
  int myDomid();

};

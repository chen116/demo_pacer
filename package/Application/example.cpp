

#include <stdlib.h>
#include <xenstore.h> // Prior to Xen 4.2.0 use xs.h

#include <heartbeats/heartbeat.h>

#include <string.h>





heartbeat_t* heart;





static const int64_t vic_win_size = 10;
static const int64_t vic_buf_depth = 1000;
static const char* vic_log_file ="vic.log";
static const int64_t vic_min_target = 100;
static const int64_t vic_max_target = 1000;

//git pull && gcc -Wall example.cpp -o out  -lxenstore -lhb-shared && ./out
void matmult(int **,int **,int **,int);

void matmult(int ** ptr1,int ** ptr2, int ** ptr3,int N){

    int i, j, k;



    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            ptr3[i][j] = 0;
            for (k = 0; k < N; k++)
                ptr3[i][j] = ptr3[i][j] + ptr1[i][k] * ptr2[k][j];
        }
    }

    return;
}


int main( int argc, const char** argv )
{
char *path;
int er;
struct xs_handle *xs;
xs_transaction_t th;
xs = xs_daemon_open();
path = xs_get_domain_path(xs, 4); 
path = (char*)realloc(path, strlen(path) + strlen("/heart_rate") + 1);
if ( path == NULL ) printf("not good\n");
strcat(path, "/heart_rate");
printf("%s\n",path);

 heart = heartbeat_init(vic_win_size, vic_buf_depth, vic_log_file, vic_min_target, vic_max_target);


    int **ptr1, **ptr2, **ptr3;
    int  col1, row2, col2;
    int N=130;
    int j,i;
    ptr1 = (int **) malloc (sizeof (int *) * N);
    ptr2 = (int **) malloc (sizeof (int *) * N);
    ptr3 = (int **) malloc (sizeof (int *) * N);
    for (i = 0; i < N; i++)
        ptr1[i] = (int *) malloc (sizeof (int) * N);
    for (i = 0; i < N; i++)
        ptr2[i] = (int *) malloc (sizeof (int) * N);
    for (i = 0; i < N; i++)
        ptr3[i] = (int *) malloc (sizeof (int) * N);

    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            ptr1[i][j] = rand ()%10;
        }
    }

    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            ptr2[i][j] = rand ()%10;
        }
    }
    for (i = 0; i < 5; ++i)
    {


        matmult(ptr1,ptr2,ptr3,N);
        matmult(ptr1,ptr2,ptr3,N);

        heartbeat(heart, 1);
        // char hr_str[10];
        // gcvt(hb_get_instant_rate(heart) , 6, hr_str);
        // printf("%s %d \n", hr_str, strlen(hr_str));
        th = xs_transaction_start(xs);
        er = xs_write(xs, th, path, "11.0", strlen("11.0"));
        xs_transaction_end(xs, th, false);
        printf("heartbeat: instant rate: %f\n",hb_get_instant_rate(heart) );
    }
    


    /** Printing the contents of third matrix. */

    printf ("\n");

th = xs_transaction_start(xs);
er = xs_write(xs, th, path, "done", strlen("done"));
xs_transaction_end(xs, th, false);


    printf ("\n");
    heartbeat_finish(heart);
    return (0);

}


// //git pull && gcc example.cpp -lhb-shared -lhrm-shared -lxenstore -std=c++11  && ./a.out
// #include <stdlib.h>
// #include <xenstore.h> // Prior to Xen 4.2.0 use xs.h

// //gcc -Wall example.c -o example.out  -lxenstore

// int main( int argc, const char** argv )
// {

// struct xs_handle *xs;
// xs_transaction_t th;
// xs = xs_daemon_open();
// printf("hi\n");
//     return (0);
// }


// //git pull && gcc example.cpp -lhb-shared -lhrm-shared -lxenstore -std=c++11  && ./a.out
// #include <xenstore.h> // Prior to Xen 4.2.0 use xs.h
// #include <stdlib.h>

// #include <stdio.h>
// #include <time.h>
// #include <heartbeats/heartbeat.h>
// #include <string.h>






// heartbeat_t* heart;





// static const int64_t vic_win_size = 10;
// static const int64_t vic_buf_depth = 1000;
// static const char* vic_log_file ="vic.log";
// static const int64_t vic_min_target = 100;
// static const int64_t vic_max_target = 1000;




// int main ()
// {

// struct xs_handle *xs;
// xs_transaction_t th;
// char *path;
// int fd;
// fd_set set;
// int er;
// struct timeval tv = {.tv_sec = 0, .tv_usec = 0 };
// char **vec;
// unsigned int num_strings;
// char * buf;
// unsigned int len;
// /* Get a connection to the daemon */
// Attempts to make a connection over the socket interface,
//  * and if it fails, then over the  xenbus interface.
//  * Mode 0 specifies read-write access, XS_OPEN_READONLY for
//  * read-only access.
// xs = xs_daemon_open();
// if ( xs == NULL ) printf("not good\n");
// /* Get the local domain path */


// path = xs_get_domain_path(xs, 4); // replace "domid" with a valid domain ID (or one which will become valid)
// if ( path == NULL ) printf("not good\n");
// /* Make space for our node on the path */
// path = (char*)realloc(path, strlen(path) + strlen("/heart_rate") + 1);
// if ( path == NULL ) printf("not good\n");
// strcat(path, "/heart_rate");
// /* Create a watch on /local/domain/%d/heart_rate. */
// // er = xs_watch(xs, path, "mytoken");
// if ( er == 0 ) printf("not good\n");
// /* We are notified of read availability on the watch via the
//  * file descriptor.
//  */
// fd = xs_fileno(xs);


//     heart = heartbeat_init(vic_win_size, vic_buf_depth, vic_log_file, vic_min_target, vic_max_target);
//     time_t t;
//     int **ptr1, **ptr2, **ptr3;
//     int  col1, row2, col2;
//     srand ((unsigned) time (&t));
//     int N=130;
//     int j,i;
//     ptr1 = (int **) malloc (sizeof (int *) * N);
//     ptr2 = (int **) malloc (sizeof (int *) * N);
//     ptr3 = (int **) malloc (sizeof (int *) * N);
//     for (i = 0; i < N; i++)
//         ptr1[i] = (int *) malloc (sizeof (int) * N);
//     for (i = 0; i < N; i++)
//         ptr2[i] = (int *) malloc (sizeof (int) * N);
//     for (i = 0; i < N; i++)
//         ptr3[i] = (int *) malloc (sizeof (int) * N);

//     for (i = 0; i < N; i++) {
//         for (j = 0; j < N; j++) {
//             ptr1[i][j] = rand ()%10;
//         }
//     }

//     for (i = 0; i < N; i++) {
//         for (j = 0; j < N; j++) {
//             ptr2[i][j] = rand ()%10;
//         }
//     }
//     for (i = 0; i < 100; ++i)
//     {


//         matmult(ptr1,ptr2,ptr3,N);
//         matmult(ptr1,ptr2,ptr3,N);

//         heartbeat(heart, 1);
//         char hr_str[10];
//         gcvt(hb_get_instant_rate(heart) , 6, hr_str);
//         printf("%s %d \n", hr_str, strlen(hr_str));
//         th = xs_transaction_start(xs);
//         er = xs_write(xs, th, path, "somestuff", strlen("somestuff"));
//         xs_transaction_end(xs, th, false);



//         printf("heartbeat: instant rate: %f\n",hb_get_instant_rate(heart) );
//     }
    
//     for (i = 0; i < 100; ++i)
//     {
//         matmult(ptr1,ptr2,ptr3,N);
//         heartbeat(heart, 1);
//         printf("    heartbeat: instant rate: %f\n",hb_get_instant_rate(heart) );
//     }

//     /** Printing the contents of third matrix. */

//     printf ("\n");
//     /* Printing the contents of third matrix. */

//     // printf ("\n\nFinal Matrix :");
//     // for (i = 0; i < N; i++) {
//     //     printf ("\n\t");
//     //     for (j = 0; j < N; j++)
//     //         printf ("%4d  ", ptr3[i][j]);
//     // }

//     printf ("\n");
//     heartbeat_finish(heart);
//     return (0);
// }
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <heartbeats/heartbeat.h>

heartbeat_t* heart;





static const int64_t vic_win_size = 10;
static const int64_t vic_buf_depth = 1000;
static const char* vic_log_file ="vic.log";
static const int64_t vic_min_target = 100;
static const int64_t vic_max_target = 1000;

void matmult(int **,int **,int **,int);

void matmult(int ** ptr1,int ** ptr2, int ** ptr3,int N){

    int i, j, k;

    for (i = 0; i < N; i++)
        ptr1[i] = (int *) malloc (sizeof (int) * N);
    for (i = 0; i < N; i++)
        ptr2[i] = (int *) malloc (sizeof (int) * N);
    for (i = 0; i < N; i++)
        ptr3[i] = (int *) malloc (sizeof (int) * N);

    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            ptr1[i][j] = rand ()%100;
        }
    }

    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            ptr2[i][j] = rand ()%100;
        }
    }

    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            ptr3[i][j] = 0;
            for (k = 0; k < N; k++)
                ptr3[i][j] = ptr3[i][j] + ptr1[i][k] * ptr2[k][j];
        }
    }

    return;
}


int main ()
{
    heart = heartbeat_init(vic_win_size, vic_buf_depth, vic_log_file, vic_min_target, vic_max_target);
    time_t t;
    int **ptr1, **ptr2, **ptr3;
    int N, col1, row2, col2;
    srand ((unsigned) time (&t));
    int N=3;
    int j,i;
    ptr1 = (int **) malloc (sizeof (int *) * N);
    ptr2 = (int **) malloc (sizeof (int *) * N);
    ptr3 = (int **) malloc (sizeof (int *) * N);
    

    for (i = 0; i < 10; ++i)
    {
        matmult(ptr1,ptr2,ptr3,N);
        heartbeat(heart, 1);
        printf("heartbeat: instant rate: %f\n",hb_get_instant_rate(heart) );
    }

    
    /** Printing the contents of third matrix. */

    printf ("\n");
    /* Printing the contents of third matrix. */

    printf ("\n\nFinal Matrix :");
    for (i = 0; i < N; i++) {
        printf ("\n\t");
        for (j = 0; j < N; j++)
            printf ("%4d", ptr3[i][j]);
    }

    printf ("\n");
    heartbeat_finish(heart);
    return (0);
}
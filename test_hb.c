//gcc test_hb.c -lhb-shared -lhrm-shared
#include <sys/time.h>
#include <unistd.h>
#include <heartbeats/heartbeat.h>

heartbeat_t* heart;





static const int64_t vic_win_size = 10;
static const int64_t vic_buf_depth = 1000;
static const char* vic_log_file ="vic.log";
static const int64_t vic_min_target = 100;
static const int64_t vic_max_target = 1000;

#include <stdio.h>
int main()
{
heart = heartbeat_init(vic_win_size, vic_buf_depth, vic_log_file, vic_min_target, vic_max_target);

	struct timeval  tv1, tv2;
int i=0;
	for (i = 0; i < 5; ++i)
	{
		gettimeofday(&tv1, NULL);
		/* stuff to do! */
heartbeat(heart, 1);


		sleep(1);

		gettimeofday(&tv2, NULL);
		printf ("Total time = %f seconds\n",
		         (double) (tv2.tv_usec - tv1.tv_usec) / 1000000 +
		         (double) (tv2.tv_sec - tv1.tv_sec));
	}

   // printf() displays the string inside quotation
heartbeat_finish(heart);

   return 0;
}

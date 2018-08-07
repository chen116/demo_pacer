#include "pacer.h"
#include <unistd.h>
//example Custom C++ Application
int main(int argc, char** argv)
{
	// create a pacer instant
	Pacer mypacer;
	// set window size for heartbeat and create heartbeat instance
	mypacer.setWindowSize(5);

	// processing loop
	for (int i = 0; i < 10; ++i)
	{
		// processing
		usleep(100000);
		// record heartbeat
		mypacer.beat();
		// write instant heart rate to xenstore
		mypacer.writeInstantHeartRate();
		// read the instant heart rate that was just written to xenstore
		printf("Insant Heartrate: %s\n",mypacer.readHeartRate());
	}

    printf("done\n");
    return 0;


}
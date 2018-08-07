#include "pacer.h"
#include <unistd.h>
//example Custom C++ Application
int main(int argc, char** argv)
{

	Pacer mypacer;
	mypacer.setWindowSize(5);

	for (int i = 0; i < 10; ++i)
	{
		usleep(100000);
		mypacer.beat();
		mypacer.writeInstantHeartRate();
		printf("Insant Heartrate: %s\n",mypacer.readHeartRate());
	}

    printf("done\n");
    return 0;


}
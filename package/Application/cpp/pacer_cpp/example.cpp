#include "pacer.h"

#include <stdio.h>
#include <unistd.h>




int main(int argc, char** argv)
{

	Pacer mypacer;
	mypacer.setWindowSize(5);

	for (int i = 0; i < 100; ++i)
	{
		usleep(100000);
		mypacer.beat();
		mypacer.writeInstantHeartRate();
		printf("Insant Heartrate: %s\n",mypacer.readHeartRate());
	}


    return 0;


}
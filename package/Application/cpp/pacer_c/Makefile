


app: clean
	-git pull
	gcc xen_comm.c -c -lhb-shared -lxenstore
	g++ vid_proc.cpp -c `pkg-config --libs opencv` -std=c++11 -lhb-shared -lxenstore
	g++ xen_comm.o vid_proc.o -o app `pkg-config --libs opencv` -std=c++11 -lhb-shared -lxenstore
clean:
	-rm -f app

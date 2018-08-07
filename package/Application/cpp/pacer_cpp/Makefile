


demo_app: clean
	-git pull
	gcc -c comm.c -lxenstore
	g++ -c pacer.cpp -lhb-shared 
	g++ -c  vid_proc.cpp  `pkg-config --libs opencv` -std=c++11 
	g++ comm.o pacer.o vid_proc.o -o vid_proc -lhb-shared -lxenstore  `pkg-config --libs opencv` -std=c++11

example: clean
	-git pull
	gcc -c comm.c -lxenstore
	g++ -c pacer.cpp -lhb-shared 
	g++ -c  example.cpp 
	g++ comm.o pacer.o example.o -o example -lhb-shared -lxenstore

clean:
	-rm -f vid_proc example *.o 




app: clean
	-git pull
	g++ -c  vid_proc.cpp  `pkg-config --libs opencv` -std=c++11  
	gcc -c comm.c -lxenstore
	g++ -c pacer.cpp -lhb-shared 
	g++ comm.o pacer.o vid_proc.o -o app -lhb-shared -lxenstore  `pkg-config --libs opencv` -std=c++11

example: clean
	-git pull
	g++ -c  example.cpp 
	gcc -c comm.c -lxenstore
	g++ -c pacer.cpp -lhb-shared 
	g++ comm.o pacer.o example.o -o example -lhb-shared -lxenstore

clean:
	-rm -f app *.o 

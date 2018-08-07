


app: clean
	-git pull
	gcc xen_comm.c -c -lhb-shared -lxenstore
	g++ vid_proc.cpp -c `pkg-config --libs opencv` -std=c++11 -lhb-shared -lxenstore
	g++ xen_comm.o vid_proc.o -o app `pkg-config --libs opencv` -std=c++11 -lhb-shared -lxenstore
clean:
	-rm -f app
git pull
g++ -c  vid_proc.cpp  `pkg-config --libs opencv` -std=c++11  
gcc -c comm.c -lxenstore
g++ -c pacer.cpp -lhb-shared 
g++ comm.o pacer.o vid_proc.o -o app -lhb-shared -lxenstore  `pkg-config --libs opencv` -std=c++11
./app
#-source=[PATH-IMAGE]  -cfg=[PATH-TO-DARKNET]/cfg/yolo.cfg -model=[PATH-TO-DARKNET]/yolo.weights   -class_names=[PATH-TO-DARKNET]/data/coco.names

git pull
g++ -c  main.cpp 
gcc -c comm.c -lhb-shared -lxenstore
g++ -c pacer.cpp -lhb-shared -lxenstore
g++ comm.o pacer.o main.o -o app -lhb-shared -lxenstore
./app


git pull
g++ -c  main.cpp 
g++ -c comm.cpp -lhb-shared -lxenstore -std=c++11
g++ comm.o main.o -o app -lhb-shared -lxenstore



app: clean
	-git pull
	#g++ yolo_object_detection.cpp -o app `pkg-config --libs opencv` -std=c++11 
	#g++ vid_proc.cpp -o app `pkg-config --libs opencv` -std=c++11 -lhb-shared -lxenstore
	g++ comm.cpp -o app `pkg-config --libs opencv` -std=c++11 -lhb-shared -lxenstore
	#gcc xen_comm.c -o app -lhb-shared -lxenstore
clean:
	-rm -f app


#-source=[PATH-IMAGE]  -cfg=[PATH-TO-DARKNET]/cfg/yolo.cfg -model=[PATH-TO-DARKNET]/yolo.weights   -class_names=[PATH-TO-DARKNET]/data/coco.names



app: clean
	g++ yolo_object_detection.cpp -o app `pkg-config --libs opencv` -std=c++11 

clean:
	-rm -f app


#-source=[PATH-IMAGE]  -cfg=[PATH-TO-DARKNET]/cfg/yolo.cfg -model=[PATH-TO-DARKNET]/yolo.weights   -class_names=[PATH-TO-DARKNET]/data/coco.names
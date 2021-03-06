import numpy as np
import cv2
import time

# net = cv2.dnn.readNet("weights/yolov3-tiny.weights", "cfg/yolov3-tiny.cfg")
net = cv2.dnn.readNet("weights/yolov3.weights", "cfg/yolov3.cfg")
data = []
with open("coco.names", "r") as f:
    data = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
outputlayers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]
warna = np.random.uniform(0, 255, size=(len(data), 3))

# 0 untuk kamera
vid = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

waktuAwal = time.time()
idFrame = 0

while True:
    _, canvas = vid.read()
    idFrame += 1
    tinggi, lebar, channels = canvas.shape

    blob = cv2.dnn.blobFromImage(canvas, 0.00392, (320, 320), (0, 0, 0), True)
    net.setInput(blob)
    outs = net.forward(outputlayers)

    idClass = []
    confidences = []
    square = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                center_x = int(detection[0] * lebar)
                center_y = int(detection[1] * tinggi)
                # cv2.circle(frame, (center_x, center_y), 10, (0, 255, 0), 2)
                w = int(detection[2] * lebar)
                h = int(detection[3] * tinggi)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                square.append([x, y, w, h])
                confidences.append(float(confidence))
                idClass.append(class_id)

    validBox = cv2.dnn.NMSBoxes(square, confidences, 0.2, 0.3)

    for i in range(len(square)):
        if i in validBox:
            x, y, w, h = square[i]
            objects = str(data[idClass[i]])
            confidence = confidences[i]
            color = warna[idClass[i]]

            cv2.rectangle(canvas, (x, y), (x + w, y + h), color, 2)
            cv2.putText(canvas, objects + " " + str(round(confidence, 2)), (x, y + 30), font, 1, color, 2)

    waktuBerjalan = time.time() - waktuAwal
    fps = idFrame / waktuBerjalan
    cv2.putText(canvas, str(round(fps, 2)), (10, 50), font, 2, (255, 255, 255), 2)
    cv2.putText(canvas, "FPS", (220, 50), font, 2, (255, 255, 255), 2)
    cv2.imshow("Kelompok 12 KB", canvas)
    key = cv2.waitKey(1)
    if key == 27:
        break

vid.release()
cv2.destroyAllWindows()

import cv2
import numpy as np
import glob
import random
import string
import os
def get_plate(img_path):
    # Load Yolo
    net = cv2.dnn.readNet("yolov3_training_last.weights", "yolov3_testing.cfg")

    # Name custom object
    classes = ["plate"]

    # Images path
    images_path = glob.glob(img_path)



    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Insert here the path of your images
    random.shuffle(images_path)
    # loop through all the images
    for img_path in images_path:
        # Loading image
        img = cv2.imread(img_path)
        img = cv2.resize(img, None, fx=0.6, fy=0.6)
        height, width, channels = img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)

        outs = net.forward(output_layers)
        noneimg = cv2.imread(img_path)
        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    # Object detected

                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        img1 = img.copy()
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in range(len(boxes)):

            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                # cv2.putText(img, label, (x, y + 30), font, 1, color, 2)
                crop_img = img1[y:y + h +8, x:x + w+8]
                crop_img = cv2.resize(crop_img, (350,250))
                crop_img = cv2.bilateralFilter(crop_img, 9, 75, 75)
                # img_path = 'E:/biensocut'
                # img_name="plate_crop".join(random.choice(string.ascii_lowercase) for i in range(5))+".jpg"
                # cv2.imwrite(os.path.join(img_path, img_name), crop_img)
                return crop_img
    return noneimg
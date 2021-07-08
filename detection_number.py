import cv2
import numpy as np
import imutils
from skimage import measure
from skimage.filters import threshold_local
def convert2Square(image):
    """
    Resize non square image(height != width to square one (height == width)
    :param image: input images
    :return: numpy array
    """

    img_h = image.shape[0]
    img_w = image.shape[1]

    # if height > width
    if img_h > img_w:
        diff = img_h - img_w
        if diff % 2 == 0:
            x1 = np.zeros(shape=(img_h, diff//2))
            x2 = x1
        else:
            x1 = np.zeros(shape=(img_h, diff//2))
            x2 = np.zeros(shape=(img_h, (diff//2) + 1))

        squared_image = np.concatenate((x1, image, x2), axis=1)
    elif img_w > img_h:
        diff = img_w - img_h
        if diff % 2 == 0:
            x1 = np.zeros(shape=(diff//2, img_w))
            x2 = x1
        else:
            x1 = np.zeros(shape=(diff//2, img_w))
            x2 = x1

        squared_image = np.concatenate((x1, image, x2), axis=0)
    else:
        squared_image = image

    return squared_image
def detection_number(img):
    V = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))[2]
    T = threshold_local(V, 15, offset=10, method="gaussian")
    thresh = (V > T).astype("uint8") * 255
    thresh = cv2.bitwise_not(thresh)
    cv2.imwrite("step2_2.png", thresh)
    thresh = imutils.resize(thresh, width=400)
    thresh = cv2.medianBlur(thresh, 5)

    # connected components analysis
    labels = measure.label(thresh, connectivity=2, background=0)
    for label in np.unique(labels):
        # if this is background label, ignore it
        if label == 0:
            continue

        # init mask to store the location of the character candidates
        mask = np.zeros(thresh.shape, dtype="uint8")
        mask[labels == label] = 255

        # find contours from mask
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(contour)

            # rule to determine characters
            aspectRatio = w / float(h)
            solidity = cv2.contourArea(contour) / float(w * h)
            heightRatio = h / float(img.shape[0])

            if 0.1 < aspectRatio < 1.0 and solidity > 0.1 and 0.35 < heightRatio < 2.0:
                # extract characters
                candidate = np.array(mask[y:y + h, x:x + w])
                square_candidate = convert2Square(candidate)
                square_candidate = cv2.resize(square_candidate, (28, 28), cv2.INTER_AREA)
                square_candidate = square_candidate.reshape((28, 28, 1))
                return square_candidate
    return 0
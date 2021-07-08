from recognition import E2E
import cv2

import time


def detect_num(img):
    # start
    start = time.time()

    # load model
    model = E2E()

    # recognize license plate
    image = model.predict(img)

    # end
    end = time.time()

    print('Model process on %.2f s' % (end - start))

    # show image
    cv2.imshow('License Plate', image)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        exit(0)

    cv2.destroyAllWindows()
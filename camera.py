import cv2
from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np,string,random
import main


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.img_counter = 0
    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()
    def shot(self):
        img_name = self.randomFileName()
        cap = cv2.VideoCapture(0)
        ret,cv_img = cap.read()
        cv2.imwrite(img_name, cv_img)
        shotCamera = [img_name, cv_img]
        self.img_counter += 1
        self.stop()
        return shotCamera
    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
    def randomFileName(self):
        letters = string.ascii_lowercase
        filename = ''
        for i in range(0, 30):
            filename += random.choice(letters)
        return 'directory_img_plate/'+filename+'.jpg'

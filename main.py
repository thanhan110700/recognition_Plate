from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2 as cv
import numpy as np
import sys,string,random,time
from datetime import datetime
import yolo_object_detection as plate
import camera,pymysql
import yolo_number_detection as number_plate
import CheckCar
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Nhận diện biển số"
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 400
        self.InitWindow()
        self.setStyleSheet("background-color:#3F3F3F")
        self.filename = None
        self.tmp = None
        self.fullImg = None
        self.old_imagePath = "None"
        self.useCamera = False
        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          passwd="",
                                          database="plate_recognition")
        self.cursor = self.connection.cursor()
        self.number_plate_curr = ''


    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)

        self.createLayout()
        self.show()
    def createLayout(self):
        # V doc H ngang
        hboxBig = QHBoxLayout()
        hbox = QHBoxLayout()

        #Button Image
        btnopenImage = QPushButton("Open Image")
        btnopenImage.setStyleSheet("Background-color:none;border: 1px solid white;border-radius:10px;height:30%;width:25%;color:white")
        btnopenImage.clicked.connect(self.getImage)
        # Button Open Cam
        btnopenCamera = QPushButton("Open Camera")
        btnopenCamera.setStyleSheet(
            "Background-color:none;border: 1px solid white;border-radius:10px;height:30%;width:25%;color:white")
        btnopenCamera.clicked.connect(self.getCamera)
        # Button Check car
        btncheckCar = QPushButton("Check Car")
        btncheckCar.setStyleSheet(
            "Background-color:none;border: 1px solid white;border-radius:10px;height:30%;width:25%;color:white")
        btncheckCar.clicked.connect(self.check_car)
        #label check
        self.querycheck = QLabel("")
        self.querycheck.setStyleSheet("color: green;")
        # Button Save/Check
        btncheckDB = QPushButton("Check")

        btncheckDB.setStyleSheet(
            "Background-color:none;border: 1px solid white;border-radius:10px;height:30%;width:25%;color:white")
        btncheckDB.clicked.connect(self.checkDB)
        #label
        lblinputnumc = QLabel('Nhập mã card: *Chỉ số')
        lblinputnumc.setStyleSheet("color: white;")
        # Input number card
        self.txtNumbercard = QLineEdit()
        self.txtNumbercard.setStyleSheet(
            "Background-color:none;border: 1px solid white;border-radius:10px;height:30%;width:25%;color:black")
        hbox.addWidget(btnopenImage,1)
        hbox.addWidget(btnopenCamera, 1)
        hbox.addWidget(btncheckCar,1)
        hbox.addWidget(self.querycheck, 1)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        # Image
        self.lblImage = QLabel()
        self.lblImage.setFixedSize(500,500)
        self.lblImage.setStyleSheet("border:1px solid white;")
        defaulImage = QPixmap('image/noimg.png')
        self.scaledefaulImage = defaulImage.scaled(50, 50)
        self.lblImage.setPixmap(self.scaledefaulImage)
        self.lblImage.setAlignment(Qt.AlignCenter)

        vbox.addWidget(self.lblImage)
        vbox.addWidget(lblinputnumc)
        vbox.addWidget(self.txtNumbercard)
        vbox.addWidget(btncheckDB)
        vbox.setAlignment(Qt.AlignCenter)

        hboxBig.addLayout(vbox)

        # Show Image Plate
        self.lblImagePlate = QLabel()
        lblanhBienso = QLabel()
        lblanhBienso.setText("Ảnh biển số")
        lblanhBienso.setStyleSheet("color:white")
        self.lblImagePlate.setFixedSize(200,150)
        self.lblImagePlate.setStyleSheet("border:1px solid white;")

        # Show old Image Plate
        self.lbloldImagePlate = QLabel()
        lbloldanhBienso = QLabel()
        lbloldanhBienso.setText("Ảnh biển số cũ")
        lbloldanhBienso.setStyleSheet("color:white")
        self.lbloldImagePlate.setFixedSize(200, 150)
        self.lbloldImagePlate.setStyleSheet("border:1px solid white;")



        # Show Plate
        self.lblPlate = QLabel()
        lblBienso = QLabel()
        lblBienso.setText("Biển số")
        lblBienso.setStyleSheet("color:white")
        self.lblPlate.setText("")
        self.lblPlate.setStyleSheet("font-size:25px;color:white")

        self.lblPlate_old = QLabel()
        lblBienso_old = QLabel()
        lblBienso_old.setText("Biển số cũ:")
        lblBienso_old.setStyleSheet("color:white")
        self.lblPlate_old.setText("")
        self.lblPlate_old.setStyleSheet("font-size:25px;color:white")

        self.lblresult = QLabel()
        result = QLabel()
        result.setText("Kết quả:")
        result.setStyleSheet("color:white")
        self.lblresult.setText("")


        vboxRight = QVBoxLayout()
        vboxRight.setAlignment(Qt.AlignTop)

        vboxRight.addWidget(lblanhBienso, 1)
        vboxRight.addWidget(self.lblImagePlate, 1)

        vboxRight.addWidget(lblBienso, 1)
        vboxRight.addWidget(self.lblPlate, 1)

        vboxRight.addWidget(lbloldanhBienso, 1)
        vboxRight.addWidget(self.lbloldImagePlate, 1)

        vboxRight.addWidget(lblBienso_old, 1)
        vboxRight.addWidget(self.lblPlate_old, 1)

        vboxRight.addWidget(result, 1)
        vboxRight.addWidget(self.lblresult, 1)
        vboxRight.addStretch(5)
        hboxBig.addLayout(vboxRight)

        self.setLayout(hboxBig)
    ################Database
    def checkDB(self):
        if(self.useCamera==False):
            self.check_old_plate(number_card=self.txtNumbercard.text(),plate_number=self.number_plate_curr)
        if(self.useCamera==True):
            print("ok")
            # OK roi
            self.th = camera.VideoThread()
            shotCamera = self.th.shot()
            self.getCamera()
            self.filename = shotCamera[0]
            self.tmp = shotCamera[1]
            self.setImage(shotCamera[1])
            self.check_old_plate(number_card=self.txtNumbercard.text(),plate_number=self.number_plate_curr)

    ####INSERT
    def insert(self,number_card,plate_number):
        img_plate = self.randomFileName()
        now = datetime.now()
        timestamps = now.strftime("%Y-%m-%d %H:%M:%S")
        print(timestamps)
        insert = "INSERT INTO `plate`(`id`, `number_card`, `plate_number`, `img_plate`,`full_img`, `check_status`,`timestamps`) VALUES (NULL, '"+number_card+"', '"+plate_number+"', '"+img_plate[0]+"','"+img_plate[1]+"', '0','"+timestamps+"');"
        print(insert)

        self.cursor.execute(insert)
        self.connection.commit()
        self.saveImage(img_plate[0])
        self.savefullImage(img_plate[1])
        self.querycheck.setText("Đã thêm")
    def update_status(self,number_card,plate_number):
        update_status = "UPDATE `plate` SET `check_status`=1 WHERE `number_card` ="+number_card+" AND `plate_number` ='"+plate_number+"' AND `check_status` = 0"
        print(update_status)

        self.cursor.execute(update_status)
        self.connection.commit()
        self.querycheck.setText("Đã cập nhật")
    ###Check old Plate
    def check_old_plate(self,number_card,plate_number):
        check_exist = "SELECT number_card,plate_number,check_status FROM plate WHERE number_card ='"+number_card+"' AND check_status=0"
        # check_exist = "SELECT number_card,plate_number,check_status FROM plate WHERE number_card ='"+number_card+"' AND plate_number ='"+plate_number+"'"
        self.cursor.execute(check_exist)
        rows = self.cursor.fetchall()
        self.connection.commit()

        if (rows==()):
            self.insert(number_card,plate_number)
        else:
            check_status = "SELECT number_card,plate_number,img_plate FROM plate WHERE number_card ='"+number_card+"' AND plate_number ='"+plate_number+"' AND check_status=0"
            self.cursor.execute(check_status)
            rows_status = self.cursor.fetchall()
            self.connection.commit()
            if (rows_status == ()):
                self.set_old_image('noimg.png', '')
                self.lblresult.setText("Không trùng khớp")
                self.lblresult.setStyleSheet("font-size:25px;color:red")
            else:
                self.update_status(number_card, plate_number)
                print("02:"+str(rows_status[0][2])+"...01:"+str(rows_status[0][1]))
                self.set_old_image(str(rows_status[0][2]),str(rows_status[0][1]))
                self.lblresult.setText("Trùng khớp")
                self.lblresult.setStyleSheet("font-size:25px;color:green")


    # BUTTON CHECK CAR
    def check_car(self):
        self.windowCheckCar = QMainWindow()
        self.ui = CheckCar.CheckCar()
        self.ui.initUI(self.windowCheckCar)
        self.windowCheckCar.show()
    #SAVE IMAGE
    def randomFileName(self):
        letters = string.ascii_lowercase
        filename = ''
        for i in range(0, 30):
            filename += random.choice(letters)
        return ['directory_img_plate/'+filename+'.jpg','directory_full_img/'+filename+'.jpg']
    def saveImage(self,filename):

        cv.imwrite(filename, self.tmp)
        print('Image saved as:', filename)
    def savefullImage(self,filename):

        cv.imwrite(filename, self.im)
        print('Image saved as:', filename)
    # Get IMAGE
    def getImage(self):
        if (self.useCamera == True):
            self.thread.stop()
            self.useCamera = False
        path_img = QFileDialog.getOpenFileName(filter="Image (*.*)")
        imagePath = path_img[0]


        if (imagePath != "" and self.old_imagePath == "None"):
            self.old_imagePath = imagePath
            self.filename = imagePath
            self.im = cv.imread(imagePath)
            self.setImage(self.im)
        if (imagePath != "" and self.old_imagePath != "None"):
            self.old_imagePath = imagePath
            self.filename = imagePath
            self.im = cv.imread(imagePath)
            self.setImage(self.im)
        if (imagePath == "" and self.old_imagePath != "None"):
            self.filename = self.old_imagePath
            self.im = cv.imread(self.old_imagePath)
            self.setImage(self.im)
        if (imagePath == "" and self.old_imagePath == "None"):
            self.lblImage.setPixmap(self.scaledefaulImage)

    def getCamera(self):
        self.useCamera = True
        # Camera
        # create the video capture thread
        self.thread = camera.VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)

        # start the thread
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.lblImage.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line,QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.lblImage.width(), self.lblImage.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    def set_old_image(self,pathOldImg,num):
        oldimg = cv.imread(pathOldImg)
        frame_old_plate = cv.cvtColor(oldimg, cv.COLOR_BGRA2RGB)
        img_old_plate = QImage(frame_old_plate, frame_old_plate.shape[1], frame_old_plate.shape[0], frame_old_plate.strides[0],
                           QImage.Format_RGB888)
        img_old_plate = img_old_plate.scaledToWidth(self.lblImagePlate.width(), Qt.SmoothTransformation)
        self.lbloldImagePlate.setPixmap(QPixmap.fromImage(img_old_plate))
        self.lblPlate_old.setText(num)
    def setImage(self,image):

        self.set_img_plate()

        if(self.useCamera==False):
            frame = cv.cvtColor(image,cv.COLOR_BGRA2RGB)
            image = QImage(frame,frame.shape[1],frame.shape[0], frame.strides[0],QImage.Format_RGB888)
            if (image.width() > image.height()):
                image = image.scaledToWidth(self.lblImage.width(), Qt.SmoothTransformation)
                self.lblImage.setPixmap(QPixmap.fromImage(image))
            if (image.width() < image.height()):
                image = image.scaledToHeight(self.lblImage.height(), Qt.SmoothTransformation)
                self.lblImage.setPixmap(QPixmap.fromImage(image))
            else:
                image = image.scaledToWidth(self.lblImage.width(), Qt.SmoothTransformation)
                self.lblImage.setPixmap(QPixmap.fromImage(image))
    def set_img_plate(self):
        img_plate = plate.get_plate(self.filename)
        self.set_plate_number(img_plate)
        self.tmp = img_plate
        frame_plate = cv.cvtColor(img_plate, cv.COLOR_BGRA2RGB)
        img_plate = QImage(frame_plate, frame_plate.shape[1], frame_plate.shape[0], frame_plate.strides[0],
                           QImage.Format_RGB888)
        img_plate = img_plate.scaledToWidth(self.lblImagePlate.width(), Qt.SmoothTransformation)
        self.lblImagePlate.setPixmap(QPixmap.fromImage(img_plate))

    def set_plate_number(self,img_plate):

        self.number_plate_curr = number_plate.number_plate(img_plate)
        self.lblPlate.setText(self.number_plate_curr)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QShortcut, QSizePolicy
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QKeySequence, QImage
import cv2
import os
import sys
import shutil
from data import Data

class UI(QMainWindow):

    def __init__(self):

        super(UI, self).__init__()

        self.ft = cv2.freetype.createFreeType2()
        self.ft.loadFontData(fontFileName='Ubuntu-R.ttf',id=0)
#/home/fyp2selfdriving/Documents/traffic_light/paper/bbox_concatenate/xml_files/concat
#/home/fyp2selfdriving/Documents/traffic_light/Yolov5/datasets/dualcam/images/test
        self.img_path = "/home/fyp2selfdriving/Documents/traffic_light/Yolov5/datasets/dualcam/images/test"
        self.save_path = ""        
        self.index = 1


        # Load the ui file
        uic.loadUi("image.ui", self)

        # Define our widgets
        self.buttonleft = self.findChild(QPushButton,"pushButton")
        self.buttonright = self.findChild(QPushButton,"pushButton_2")
        self.labelnarrow = self.findChild(QLabel, "label")

        self.labelnarrowtext = self.findChild(QLabel, "label_narrow")


        # Click the dropdown box
        self.buttonleft.clicked.connect(self.clicker_left)
        self.buttonright.clicked.connect(self.clicker_right)
        shortcutleft = QShortcut(QKeySequence("Left"), self)
        shortcutright = QShortcut(QKeySequence("Right"), self)

        shortcutleft.activated.connect(self.clicker_left)
        shortcutright.activated.connect(self.clicker_right)

        self.view_img()

        # Show the App

        self.show()

    def clicker_left(self):
        if self.index > 1:
            self.index -= 1

        self.view_img()

    def clicker_right(self):
        self.index += 1
        try:
            self.view_img()
        except:
            self.index -= 1
            self.view_img()

    def view_img(self):
        fnamenarrow = self.img_path + "/wide_t1_" + self.convert_to_str(self.index) + ".jpg"

        narrow_image_data = Data(fnamenarrow)
        bbox_narrow = self.process_image(narrow_image_data,False,True, self.ft)
        bbox_narrow = QImage(bbox_narrow, bbox_narrow.shape[1],\
                            bbox_narrow.shape[0], bbox_narrow.shape[1] * 3,QImage.Format_RGB888)

        self.pixmapnarrow = QPixmap(bbox_narrow)

        self.labelnarrowtext.setText("t1_" + self.convert_to_str(self.index) + ".xml")

        self.labelnarrow.setPixmap(self.pixmapnarrow.scaled(self.labelnarrow.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation))

        self.labelnarrow.setScaledContents = True

        self.labelnarrow.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)


    # def save_imgs(self):
    #     fnamenarrow = self.file_path + "2_narrow/narrow_2_" + self.convert_to_str(self.index) + ".jpg"
    #     fnamewide = self.file_path + "2_wide/wide_2_" + self.convert_to_str(self.index) + ".jpg"
    #     fnamenarrowsave = self.save_path + "narrow_2_" + self.convert_to_str(self.index) + ".jpg"
    #     fnamewidesave = self.save_path + "wide_2_" + self.convert_to_str(self.index) + ".jpg"
    #     shutil.copyfile(fnamenarrow , fnamenarrowsave)
    #     shutil.copyfile(fnamewide , fnamewidesave)

    def process_image(self,image_data,with_mask=False,with_bbox=False,fontft=None):
        image_data.image_path = image_data.image_path
        print(image_data.image_path)

        
        image = cv2.imread(image_data.image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if with_bbox:
            for ann in image_data.annotations:
                box_color = (0, 255, 0)  #Green
                if ann.difficult or ann.truncated:
                    box_color = (0, 0, 255) #Red
                image = cv2.rectangle(image, (ann.xmin, ann.ymin), (ann.xmax, ann.ymax), box_color, 2)
                if (ann.xmax - ann.xmin)<20:
                    fontft.putText(img=image, text=ann.name, org=(ann.xmin-20, ann.ymin+15), fontHeight=15, color=(255, 0, 255), thickness=-1, line_type=cv2.LINE_AA, bottomLeftOrigin=True)
                else:
                    if ann.name == 'Count-down' or ann.name == 'Empty-count-down':
                        fontft.putText(img=image, text=ann.name, org=(ann.xmin-20, ann.ymax+15), fontHeight=40, color=(255, 0, 255), thickness=-1, line_type=cv2.LINE_AA, bottomLeftOrigin=True)
                    else:
                        fontft.putText(img=image, text=ann.name, org=(ann.xmin-20, ann.ymin+15), fontHeight=40, color=(255, 0, 255), thickness=-1, line_type=cv2.LINE_AA, bottomLeftOrigin=True)

        return image


    def convert_to_str(self,ind):
        return '{0:03}'.format(ind)

# Initialize The App

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()

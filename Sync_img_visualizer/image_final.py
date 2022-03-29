from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QShortcut, QSizePolicy
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QKeySequence, QImage
import cv2
import os
import glob
import sys
import shutil
from data import Data

class UI(QMainWindow):

    def __init__(self):

        super(UI, self).__init__()

        self.ft = cv2.freetype.createFreeType2()
        self.ft.loadFontData(fontFileName='Ubuntu-R.ttf',id=0)

        self.file_path = "/home/fyp2selfdriving/Documents/traffic_light/Yolov5/datasets/Finalized_set/DualCam/samples"
        self.save_path = ""        
        self.index = 1

        self.img_list  = self.getImagesInDir(self.file_path + "/images")
        self.img_list.sort()

        self.narrow_img_list = self.img_list[:int(len(self.img_list)/2)]
        self.wide_img_list = self.img_list[int(len(self.img_list)/2):]

        # Load the ui file
        uic.loadUi("image.ui", self)

        # Define our widgets
        self.buttonleft = self.findChild(QPushButton,"pushButton")
        self.buttonright = self.findChild(QPushButton,"pushButton_2")
        self.labelnarrow = self.findChild(QLabel, "label")
        self.labelwide = self.findChild(QLabel, "label_2")
        self.labelnarrowtext = self.findChild(QLabel, "label_narrow")
        self.labelwidetext = self.findChild(QLabel, "label_wide")

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
        _, fnamenarrow = os.path.split(self.narrow_img_list[self.index-1])
        _, fnamewide = os.path.split(self.wide_img_list[self.index-1])

        narrow_image_data = Data(fnamenarrow, self.file_path)
        bbox_narrow = self.process_image(narrow_image_data,False,True, self.ft)
        bbox_narrow = QImage(bbox_narrow, bbox_narrow.shape[1],\
                            bbox_narrow.shape[0], bbox_narrow.shape[1] * 3,QImage.Format_RGB888)

        wide_image_data = Data(fnamewide, self.file_path)
        bbox_wide = self.process_image(wide_image_data,False,True, self.ft)
        bbox_wide = QImage(bbox_wide, bbox_wide.shape[1],\
                            bbox_wide.shape[0], bbox_wide.shape[1] * 3,QImage.Format_RGB888)

        self.pixmapnarrow = QPixmap(bbox_narrow)
        self.pixmapwide = QPixmap(bbox_wide)
        self.labelnarrowtext.setText(fnamenarrow)
        self.labelwidetext.setText(fnamewide)
        self.labelnarrow.setPixmap(self.pixmapnarrow.scaled(self.labelnarrow.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation))
        self.labelwide.setPixmap(self.pixmapwide.scaled(self.labelwide.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation))
        self.labelnarrow.setScaledContents = True
        self.labelwide.setScaledContents = True
        self.labelnarrow.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
        self.labelwide.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)


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


    def getImagesInDir(self,dir_path):
        image_list = []
        for filename in glob.glob(dir_path + '/*.jpg'):
            image_list.append(filename)

        return image_list

# Initialize The App

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()

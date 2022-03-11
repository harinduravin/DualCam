import os
from bs4 import BeautifulSoup


class Entity():
    def __init__(self, name, xmin, xmax, ymin, ymax, difficult, truncated):
        self.name = name
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.difficult = difficult
        self.truncated = truncated


class Data():
    def __init__(self, image_path):
        # self.image_name = image_name
        self.image_path = image_path
        rootpath,filename = os.path.split(image_path)
        self.annotation_path = '/home/fyp2selfdriving/Documents/traffic_light/paper/combined_gt/finalized_1/xmlfiles/wide_'+filename[5:-4] + ".xml"
        # self.mask_path=os.path.join(root_dir,'SegmentationClass',image_name+'.png')
        print(self.annotation_path)
        self.annotations = self.load_masks()

    def load_masks(self):
        annotations = []
        # print('annotation path - ', self.annotation_path)
        xml_content = open(self.annotation_path).read()
        bs = BeautifulSoup(xml_content, 'xml')
        objs = bs.findAll('object')
        for obj in objs:
            obj_name = obj.findChildren('name')[0].text
            # difficult = int(obj.findChildren('difficult')[0].contents[0])
            # truncated = int(obj.findChildren('truncated')[0].contents[0])
            bbox = obj.findChildren('bndbox')[0]
            # print('value error ------', type(bbox.findChildren('xmin')[0].contents[0]))
            xmin = int(float(bbox.findChildren('xmin')[0].contents[0]))
            ymin = int(float(bbox.findChildren('ymin')[0].contents[0]))
            xmax = int(float(bbox.findChildren('xmax')[0].contents[0]))
            ymax = int(float(bbox.findChildren('ymax')[0].contents[0]))
            # print('coordinates - ', xmin, ymin, xmax, ymax)
            annotations.append(Entity(obj_name, xmin, xmax, ymin, ymax, '', ''))
        return annotations

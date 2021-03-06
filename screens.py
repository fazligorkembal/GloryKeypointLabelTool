import cv2
import utils

class screen:
    def __init__(self):
        self.color_green = (0, 255, 0)
        self.color_red   = (0, 0, 255)
        self.color_blue  = (255, 0, 0)
        self.thickness = 1

    def annotation_screen(self, image, annotations = None, original_resolution=None,new_resolution=None, line_center=None, selected_point=None):
        
        if line_center != None:
            image = cv2.line(image, (line_center[0], 0), (line_center[0], new_resolution[1]), self.color_green, self.thickness) 
            image = cv2.line(image, (0, line_center[1]), (new_resolution[0], line_center[1]), self.color_green, self.thickness) 
        
        if selected_point != None:
            image = cv2.circle(image, selected_point['location'], self.thickness, self.color_red, self.thickness)
            image = cv2.rectangle(image, selected_point['location'], line_center, self.color_red, self.thickness)
        
        print("XXXXXXX")
        if original_resolution == None:
            print('original_resolution')
        if new_resolution == None:
            print("new resolution")


        if annotations != None:
            for annotation in annotations:
                bbox = annotation['bbox']
                xmin = bbox[0]
                ymin = bbox[1]
                xmax = bbox[0] + bbox[2]
                ymax = bbox[1] + bbox[3]

                xmin, ymin = utils.reshapeResizeSizes(xmin, ymin, original_resolution, new_resolution)
                xmax, ymax = utils.reshapeResizeSizes(xmax, ymax, original_resolution, new_resolution)

                image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), self.color_green, self.thickness)

        return image
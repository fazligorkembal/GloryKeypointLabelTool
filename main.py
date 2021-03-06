import cv2
import utils
import json
import dataTree
import screens
class Tv:
    def __init__(self, images_main_folder, json_file_path):
        self.app_name = "GloryKeypointLabelingtool"
        self.images_main_folder = images_main_folder
        self.json_file_path = json_file_path

        self.data = dataTree.data(json_file_path)
        all_image_paths = utils.get_all_images(self.images_main_folder)
        self.all_image_json_indexes = self.data.getImageIndexes(all_image_paths)

        self.current_index = 0
        self.selected_image = None
        self.selected_image_id = None

        self.original_resolution = None
        self.new_resolution = (1280, 720)

        self.selected_original_image = None

        self.screens = screens.screen()
        self.screen_name = ['annotation_screen']
        self.selected_point = None

        self.temp_category_name = "XXX"


    def start(self):
        while True:
            selected_image_path = self.data.data['images'][self.current_index]['file_name']
            self.selected_original_image = cv2.imread(selected_image_path)
            self.selected_image_annotations = self.data.getImageAnnotationsWithImageIndex(self.current_index)
            self.original_resolution = (self.selected_original_image.shape[1], self.selected_original_image.shape[0])

            pressed_key = self.reflesh(wait=True, annotations=self.selected_image_annotations, selected_point=self.selected_point)
            if self.controller(pressed_key):
                break
        
    
    def reflesh(self, wait=False, annotations=None, line_center= None, selected_point=None):
        image = cv2.resize(self.selected_original_image, self.new_resolution)

        if self.screen_name == ['annotation_screen']:
            image = self.screens.annotation_screen(image, annotations=annotations,line_center=line_center, selected_point=selected_point, original_resolution=self.original_resolution, new_resolution=self.new_resolution)

        cv2.imshow(self.app_name, image)

        if wait:
            cv2.setMouseCallback(self.app_name, self.clickListener)
            return cv2.waitKey(0)
        else:
            return None
        

    def clickListener(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            if self.screen_name == ['annotation_screen'] or self.screen_name == ['keypoint_screen']:
                None

        if event == cv2.EVENT_LBUTTONDOWN:
            print("ToDo: Check clicked on exist point")

            if self.screen_name == ['annotation_screen']:

                if self.selected_point == None:
                    self.selected_point = {}
                    self.selected_point['point_name'] = 'min'
                    self.selected_point['location'] = (x, y)
                else:
                    if self.selected_point['point_name'] == 'min':
                        xmin, ymin = self.selected_point['location']
                        xmax, ymax = (x, y)
                        bbox_width = xmax - xmin
                        bbox_height = ymax - ymin

                        xmin, ymin = utils.reshapeOriginalSizes(xmin, ymin, self.original_resolution, self.new_resolution)
                        bbox_width, bbox_height = utils.reshapeOriginalSizes(bbox_width, bbox_height, self.original_resolution, self.new_resolution)
                        bbox = (xmin, ymin, bbox_width, bbox_height)

                        self.data.addAnnotationWithImageJsonIndex(self.current_index, bbox, self.temp_category_name)
                        self.selected_image_annotations = self.data.getImageAnnotationsWithImageIndex(self.current_index)
                        self.selected_point = None

        self.reflesh(wait=False, annotations=self.selected_image_annotations, line_center=(x, y), selected_point=self.selected_point)







    def controller(self, pressed_key):
        if pressed_key & 0xFF == ord('q'):
            return True


        if self.screen_name == ['annotation_screen']:
            if pressed_key & 0xFF == ord('d'):
                if self.current_index < len(self.all_image_json_indexes) - 1:
                    self.current_index += 1
                else:
                    self.current_index =  len(self.all_image_json_indexes) -1
            if pressed_key & 0xFF == ord('a'):
                if self.current_index > 0:
                    self.current_index -= 1
                else:
                    self.current_index = 0
            
            if pressed_key & 0xFF == 27:
                self.selected_point = None


        self.selected_point = None









if __name__ == '__main__':
    tv = Tv('/home/gorkem/Documents/GloryKeypointLabelTool/dataset', '/home/gorkem/Documents/GloryKeypointLabelTool/testx2.json')
    #tv = Tv('/home/gorkem/Documents/GloryKeypointLabelTool/dataset', '/home/gorkem/Documents/GloryKeypointLabelTool/test.json')

    tv.start()
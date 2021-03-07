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
        self.selected_button = None
        self.selected_annotation = None



    def start(self):
        while True:
            selected_image_path = self.data.data['images'][self.current_index]['file_name']
            self.selected_original_image = cv2.imread(selected_image_path)
            self.selected_image_annotations = self.data.getImageAnnotationsWithImageIndex(self.current_index)
            self.original_resolution = (self.selected_original_image.shape[1], self.selected_original_image.shape[0])

            pressed_key = self.reflesh(wait=True, annotations=self.selected_image_annotations, selected_point=self.selected_point)
            if self.menu_controller(pressed_key=pressed_key):
                break
        
    
    def reflesh(self, wait=False, annotations=None, line_center= None, selected_point=None, new_name=None, selected_button=None, selected_annotation=None):
        image = cv2.resize(self.selected_original_image, self.new_resolution)

        if self.screen_name == ['annotation_screen']:
            image = self.screens.annotation_screen(image, annotations=annotations,line_center=line_center, selected_point=selected_point, original_resolution=self.original_resolution, new_resolution=self.new_resolution)

        if self.screen_name == ['option_screen']:
            all_categories = self.data.data['categories']
            image, self.option_buttons = self.screens.option_screen(image,new_name=new_name, selected_button=selected_button, all_categories=all_categories, selected_annotation=selected_annotation)

        cv2.imshow(self.app_name, image)

        if wait:
            cv2.setMouseCallback(self.app_name, self.clickListener)
            return cv2.waitKey(0)
        else:
            return None
        

    def clickListener(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            
            if self.screen_name == ['annotation_screen']:
                print("ToDo: Check clicked on exist point")
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


                        self.data.addAnnotationWithImageJsonIndex(self.current_index, bbox, self.selected_annotation['index'])
                        self.selected_image_annotations = self.data.getImageAnnotationsWithImageIndex(self.current_index)
        
                    #self.reflesh(wait=False, annotations=self.selected_image_annotations, line_center=(x, y))

            elif self.screen_name == ['option_screen'] and self.selected_button == None:
                for option_button in self.option_buttons:
                    box = option_button['location']
                    if x > box[0] and x < box[2] and y > box[1] and y < box[3]:
                        
                        if option_button['name'] != 'annotation':
                            self.selected_button = option_button
                            new_string = self.getStringFromView()
                            if self.selected_button['name'] == 'new_annotation' and new_string != None:
                                self.data.addCategory(new_string)
                            elif self.selected_button['name'] == 'new_keypoint' and new_string != None:
                                if self.selected_annotation != None:
                                    self.data.addKeypointWithCategoryIndex(self.selected_annotation['index'], new_string)
                                    
                            self.selected_button = None
                        else:
                            if self.selected_annotation != option_button:
                                self.selected_annotation = option_button
                                self.selected_button = None
                            else:
                                self.selected_annotation = None
                            
        self.reflesh(wait=False, annotations=self.selected_image_annotations, line_center=(x, y),selected_button=self.selected_button, selected_annotation=self.selected_annotation)


    def getStringFromView(self):
        new_string = ""
        while True:
            pressed_key = self.reflesh(wait=True, new_name=new_string, selected_button=self.selected_button, selected_annotation=self.selected_annotation)

            if pressed_key & 0xFF == 8 and new_string != "":
                    new_string = new_string[: -1]
                    self.reflesh(wait=False, new_name=new_string, selected_button=self.selected_button, selected_annotation=self.selected_annotation)
            elif pressed_key & 0xFF == 13 and new_string != "":
                    self.reflesh(wait=False)
                    return new_string
            elif pressed_key & 0xFF == 27:
                self.reflesh(wait=False)
                #self.selected_button = None
                return None
                break
            else:
                new_string = new_string + chr(pressed_key)
                self.reflesh(wait=False, new_name=new_string, selected_button=self.selected_button, selected_annotation=self.selected_annotation)


    def menu_controller(self, pressed_key=None):
        if pressed_key & 0xFF == ord('q'):
            return True

        if pressed_key & 0xFF == ord('e'):
            if self.screen_name != ['option_screen']:
                self.screen_name = ['option_screen']
            else:
                self.screen_name = ['annotation_screen']


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

        self.option_buttons = None
        self.selected_point = None








if __name__ == '__main__':
    tv = Tv('/home/gorkem/Documents/GloryKeypointLabelTool/dataset', '/home/gorkem/Documents/GloryKeypointLabelTool/testx2.json')
    #tv = Tv('/home/gorkem/Documents/GloryKeypointLabelTool/dataset', '/home/gorkem/Documents/GloryKeypointLabelTool/test.json')

    tv.start()
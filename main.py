import cv2
import utils
import dataTree
import screens
import time
import argparse


class Tv:
    def __init__(self, images_main_folder, json_file_path):
        self.app_name = "GloryKeypointLabelingtool"
        self.images_main_folder = images_main_folder
        self.json_file_path = json_file_path
        self.data = dataTree.data(json_file_path)
        self.all_image_paths = utils.get_all_images(self.images_main_folder)

        self.selected_image = None
        self.selected_image_id = None
        self.original_resolution = None
        self.new_resolution = (1280, 720)
        self.selected_original_image = None
        
        self.screens = screens.screen()
        self.current_index = 0
        self.screen_name = ['help_screen']
        self.selected_point = None
        self.selected_button = None
        self.selected_category = None
        self.keypoint_visible = 2
        self.added_keypoint_count = 0
        self.selected_image_data = None
        self.editable_point_radius = 3.0
    
    def start(self):
        if len(self.all_image_paths) > 0:
            while True:
                selected_image_path = self.all_image_paths[self.current_index]
                self.selected_original_image =  cv2.imread(selected_image_path)
                self.original_resolution = (self.selected_original_image.shape[1], self.selected_original_image.shape[0])
                self.selected_image_data, self.selected_image_annotations = self.data.GetImageData(selected_image_path, self.original_resolution)
                
                pressed_key = self.reflesh(wait=True, annotations=self.selected_image_annotations, selected_point=self.selected_point, selected_category=self.selected_category, all_categories=self.data.data['categories'])
                
                if self.menu_controller(pressed_key=pressed_key):
                    break
   


    def reflesh(self, wait=False, annotations=None, line_center= None, selected_point=None, new_name=None, selected_button=None, selected_category=None, all_categories=None):
        image = cv2.resize(self.selected_original_image, self.new_resolution)

        if self.screen_name == ['annotation_screen'] or self.screen_name == ['keypoint_screen']:
            image = self.screens.annotation_screen(image, annotations=annotations,line_center=line_center, selected_category=self.selected_category, selected_point=selected_point, original_resolution=self.original_resolution, 
                                                   new_resolution=self.new_resolution, all_categories=all_categories, process=self.screen_name, keypoint_num=self.added_keypoint_count, visible=self.keypoint_visible)

        if self.screen_name == ['option_screen']:
            all_categories = self.data.data['categories']
            image, self.option_buttons = self.screens.option_screen(image, new_name=new_name, selected_button=selected_button, all_categories=all_categories, selected_category=selected_category)

        if self.screen_name == ['help_screen']:
            self.screens.help_screen(image)

        cv2.imshow(self.app_name, image)

        if wait:
            cv2.setMouseCallback(self.app_name, self.clickListener)
            return cv2.waitKey(0)
        else:
            return None

    def clickListener(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.screen_name == ['option_screen'] and self.selected_button == None:
                for option_button in self.option_buttons:
                    box = option_button['location']
                    if x > box[0] and x < box[2] and y > box[1] and y < box[3]:
                        if option_button['name'] == 'new_annotation' or option_button['name'] == 'new_keypoint':
                            self.selected_button = option_button
                            new_string = self.getStringFromView()
                            if self.selected_button['name'] == 'new_annotation' and new_string != None:
                                self.data.addCategory(new_string)
                            elif self.selected_button['name'] == 'new_keypoint' and new_string != None:
                                if self.selected_category != None:
                                    self.data.addKeypointToCategoriesWithCategoryIndex(self.selected_category['index'], new_string)
                                    
                            self.selected_button = None
                        elif option_button['name'] == 'annotation':
                            if self.selected_category != option_button:
                                self.selected_category = option_button
                                self.selected_button = None
                            else:
                                self.selected_category = None
                        elif option_button['name'] == 'resolution':
                            self.new_resolution = option_button['resolution']
                            
                self.reflesh(wait=False, annotations=self.selected_image_annotations, selected_button=self.selected_button, selected_category=self.selected_category)

            if self.screen_name == ['annotation_screen']:
                if self.selected_point == None:
                    self.selected_point = {}
                    self.selected_point['process_name'] = 'annotation'
                    self.selected_point['point_name'] = 'min'
                    self.selected_point['location'] = (x, y)

                    distance, hold_point = utils.getNearestPoint(self.selected_image_annotations, x, y, self.original_resolution, self.new_resolution)
                    
                    if distance < self.editable_point_radius:
                        self.selected_point = hold_point

                else:
                    if self.selected_point['process_name'] == 'annotation':
                        xmin, ymin = self.selected_point['location']
                        xmax, ymax = (x, y)
                        bbox_width = xmax - xmin
                        bbox_height = ymax - ymin

                        xmin, ymin = utils.reshapeToOriginalResolution(xmin, ymin, self.original_resolution, self.new_resolution)
                        bbox_width, bbox_height = utils.reshapeToOriginalResolution(bbox_width, bbox_height, self.original_resolution, self.new_resolution)
                        bbox = (xmin, ymin, bbox_width, bbox_height)

                        self.selected_image_annotations = self.data.addAnnotationWithImageID(self.selected_category['index'], self.selected_image_data['id'], self.original_resolution, bbox, self.selected_image_annotations)
                        if len(self.data.data['categories'][self.selected_category['index']]['keypoints']) > 0:
                            self.screen_name = ['keypoint_screen']

                    elif self.selected_point['process_name'] == 'edit':
                        newx, newy = utils.reshapeToOriginalResolution(x, y, self.original_resolution, self.new_resolution)
                        if self.selected_point['point_name'] == 'min':
                            bbox = list(self.selected_image_annotations[self.selected_point['annotation_index']]['bbox'])
                            xmin, ymin, xmax, ymax = bbox
                            xmax = xmin + xmax
                            ymax = ymin + ymax
                            bbox = [newx, newy, xmax - newx, ymax - newy]
                            self.selected_image_annotations[self.selected_point['annotation_index']]['bbox'] = list(bbox)
                            self.selected_image_annotations[self.selected_point['annotation_index']]['bbox'] = bbox

                        elif self.selected_point['point_name'] == 'max':
                            bbox = list(self.selected_image_annotations[self.selected_point['annotation_index']]['bbox'])
                            bbox[2] = newx - bbox[0]
                            bbox[3] = newy - bbox[1]
                            self.selected_image_annotations[self.selected_point['annotation_index']]['bbox'] = list(bbox)
                        
                        elif self.selected_point['point_name'] == 'keypoint':
                            self.selected_image_annotations[self.selected_point['annotation_index']]['keypoints'][self.selected_point['keypoint_index'] - 2] = newx
                            self.selected_image_annotations[self.selected_point['annotation_index']]['keypoints'][self.selected_point['keypoint_index'] - 1] = newy
                            self.selected_image_annotations[self.selected_point['annotation_index']]['keypoints'][self.selected_point['keypoint_index']] = self.keypoint_visible

                    self.selected_point = None
                self.reflesh(wait=False, annotations=self.selected_image_annotations, line_center=(x,y), all_categories=self.data.data['categories']) 



            elif self.screen_name == ['keypoint_screen']:
                num_keypoints = len(self.data.data['categories'][self.selected_category['index']]['keypoints'])
                
                if self.added_keypoint_count < num_keypoints:
                    newx, newy = utils.reshapeToOriginalResolution(x, y, self.original_resolution, self.new_resolution)
                    self.selected_image_annotations = self.data.addKeypoint( self.selected_image_annotations, newx, newy, self.keypoint_visible)
                    self.added_keypoint_count += 1
                    self.reflesh(wait=False, annotations=self.selected_image_annotations, line_center=(x,y), all_categories=self.data.data['categories']) 
   
                if self.added_keypoint_count == num_keypoints:
                    self.added_keypoint_count = 0
                    self.screen_name = ['annotation_screen']


        if event == cv2.EVENT_MOUSEMOVE and (self.screen_name == ['annotation_screen'] or self.screen_name == ['keypoint_screen']):
            self.reflesh(wait=False, annotations=self.selected_image_annotations, selected_point=self.selected_point, line_center=(x,y), all_categories=self.data.data['categories']) 

    def menu_controller(self, pressed_key=None):
        if pressed_key & 0xFF == ord('q'):
            self.data.save()
            return True

        if pressed_key & 0xFF == ord('e'):
            if self.screen_name != ['option_screen']:
                self.screen_name = ['option_screen']
            else:
                self.screen_name = ['annotation_screen']
        
        if pressed_key & 0xFF == ord('h'):
            if self.screen_name != ['help_screen']:
                self.screen_name = ['help_screen']
            else:
                self.screen_name = ['annotation_screen']

        if pressed_key & 0xFF == 45:
            self.screens.decreaseCircle()
        
        if pressed_key & 0xFF == 43:
            self.screens.increaseCircle()

        if pressed_key & 0xff == 49 and self.screen_name != ['option_screen'] and self.screen_name != ['help_screen']:
            self.keypoint_visible = 2
        
        if pressed_key & 0xFF == 50 and self.screen_name != ['option_screen'] and self.screen_name != ['help_screen']:
            self.keypoint_visible = 1
        
        if pressed_key & 0xFF == 51 and self.screen_name != ['option_screen'] and self.screen_name != ['help_screen']:
            self.keypoint_visible = 0

        if pressed_key & 0xFf == 255 and self.selected_point != None and self.selected_point['process_name'] == 'edit':
            self.data.deleteAnnotation(self.selected_image_annotations[self.selected_point['annotation_index']])

        if self.screen_name == ['annotation_screen']:
            if pressed_key & 0xFF == ord('d'):
                if self.current_index < len(self.all_image_paths) - 1:
                    self.current_index += 1
                else:
                    self.current_index =  len(self.all_image_paths) -1
            if pressed_key & 0xFF == ord('a'):
                if self.current_index > 0:
                    self.current_index -= 1
                else:
                    self.current_index = 0
            if pressed_key & 0xFF == 27:
                self.selected_point = None

        self.option_buttons = None
        self.selected_point = None


    def getStringFromView(self):
        new_string = ""
        while True:
            pressed_key = self.reflesh(wait=True, new_name=new_string, selected_button=self.selected_button, selected_category=self.selected_category)

            if pressed_key & 0xFF == 8 and new_string != "":
                    new_string = new_string[: -1]
                    self.reflesh(wait=False, new_name=new_string, selected_button=self.selected_button, selected_category=self.selected_category)
            elif pressed_key & 0xFF == 13 and new_string != "":
                    self.reflesh(wait=False)
                    return new_string
            elif pressed_key & 0xFF == 27:
                self.reflesh(wait=False, selected_category=self.selected_category)
                return None
                break
            else:
                new_string = new_string + chr(pressed_key)
                self.reflesh(wait=False, new_name=new_string, selected_button=self.selected_button, selected_category=self.selected_category)


if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="Keypoint Labeling Tool")
    parser.add_argument("--image_folder", type=str, help='Root images folder path', required=True)
    parser.add_argument("--json_file", type=str, help='Json path, if the file does not exist, it will be created', required=True)
    args = parser.parse_args()

    tv = Tv(args.image_folder, args.json_file)
    tv.start()
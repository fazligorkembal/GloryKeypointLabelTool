import cv2
import utils

class screen:
    def __init__(self):
        self.color_green = (0, 255, 0)
        self.color_red   = (0, 0, 255)
        self.color_blue  = (255, 0, 0)
        self.color_grey = (125, 125, 125)
        self.thickness = 1
        self.button_locations = []
    
    
    def addButtonLocation(self, name=None, index=None, location=None, resolution=None):
        temp = {}
        temp['name'] = name
        temp['index'] = index
        temp['location'] = location
        temp['resolution'] = resolution
        self.button_locations.append(temp)
    
    def increaseCircle(self):
        if self.thickness < 5:
            self.thickness += 1
    

    def decreaseCircle(self):
        if self.thickness > 1:
            self.thickness -= 1


    def annotation_screen(self, image, annotations = None, original_resolution=None,new_resolution=None, line_center=None, selected_point=None, all_categories=None):
        image = cv2.putText(image, 'Annotation Screen', (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, self.color_blue, 2, cv2.LINE_AA)
        if line_center != None:
            image = cv2.line(image, (line_center[0], 0), (line_center[0], new_resolution[1]), self.color_green, self.thickness) 
            image = cv2.line(image, (0, line_center[1]), (new_resolution[0], line_center[1]), self.color_green, self.thickness) 
        
        if selected_point != None and selected_point['process_name'] == 'annotation':
            image = cv2.circle(image, selected_point['location'], self.thickness, self.color_red, self.thickness)
            image = cv2.rectangle(image, selected_point['location'], line_center, self.color_red, self.thickness)

        print(selected_point)

        if annotations != None or annotations != []:
            for annotation_index, annotation in enumerate(annotations):
                bbox = annotation['bbox']
                xmin = bbox[0]
                ymin = bbox[1]
                xmax = bbox[0] + bbox[2]
                ymax = bbox[1] + bbox[3]



                xmin, ymin = utils.reshapeToNewResolution(xmin, ymin, original_resolution, new_resolution)
                xmax, ymax = utils.reshapeToNewResolution(xmax, ymax, original_resolution, new_resolution)

                image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), self.color_green, self.thickness)
                image = cv2.putText(image, all_categories[annotation['category_id'] - 1]['name'], (xmin + 10, ymin + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_green, 1, cv2.LINE_AA)
                if selected_point != None and selected_point['process_name'] == 'edit' and selected_point['annotation_index'] == annotation_index and selected_point['point_name'] == 'min':
                    image = cv2.circle(image, (xmin, ymin), self.thickness, self.color_red, self.thickness)
                else:
                    image = cv2.circle(image, (xmin, ymin), self.thickness, self.color_green, self.thickness)
                if selected_point != None and selected_point['process_name'] == 'edit' and selected_point['annotation_index'] == annotation_index and selected_point['point_name'] == 'max':
                    image = cv2.circle(image, (xmax, ymax), self.thickness, self.color_red, self.thickness)
                else:
                    image = cv2.circle(image, (xmax, ymax), self.thickness, self.color_green, self.thickness)

                

                axis_hold = []
                for axis_index, axis in enumerate(annotation['keypoints']):
                    axis_hold.append(axis)
                    
                    if len(axis_hold) == 3:
                        x = axis_hold[0]
                        y = axis_hold[1]
                        x, y = utils.reshapeToNewResolution(x, y, original_resolution, new_resolution)
                        visible = axis_hold[2]
                        axis_hold = []

                        if selected_point != None and selected_point['process_name'] == 'edit' and selected_point['point_name'] == 'keypoint' and selected_point['annotation_index'] == annotation_index and selected_point['keypoint_index'] == axis_index:
                            image = cv2.circle(image, (x, y), self.thickness, self.color_red, self.thickness)
                        elif visible == 2:
                            image = cv2.circle(image, (x, y), self.thickness, self.color_green, self.thickness)
                        elif visible == 1:
                            image = cv2.circle(image, (x, y), self.thickness, self.color_blue, self.thickness)
                        else:
                            image = cv2.circle(image, (x, y), self.thickness, self.color_grey, self.thickness)
                        



        return image


    def option_screen(self, image, selected_button=None, new_name=None, all_categories=None, selected_category=None):
        self.button_locations = []


        image = cv2.putText(image, 'Option Screen', (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, self.color_blue, 2, cv2.LINE_AA)
        
        if selected_button == None:
            image = cv2.putText(image, 'New Annotation', (1000, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, self.color_blue, 1, cv2.LINE_AA)
            image = cv2.rectangle(image, (990, 10), (1250, 50), self.color_blue, 1)
            image = cv2.putText(image, 'New Keypoint', (1000, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, self.color_blue, 1, cv2.LINE_AA)
            image = cv2.rectangle(image, (990, 60), (1220, 100), self.color_blue, 1)
        else:
            if selected_button['name'] == 'new_annotation':
                image = cv2.putText(image, 'New Annotation', (1000, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, self.color_green, 1, cv2.LINE_AA)
                image = cv2.rectangle(image, (990, 10), (1250, 50), self.color_green, 1)
                image = cv2.putText(image, 'New Keypoint', (1000, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, self.color_blue, 1, cv2.LINE_AA)
                image = cv2.rectangle(image, (990, 60), (1220, 100), self.color_blue, 1)
            elif selected_button['name'] == 'new_keypoint':
                image = cv2.putText(image, 'New Annotation', (1000, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, self.color_blue, 1, cv2.LINE_AA)
                image = cv2.rectangle(image, (990, 10), (1250, 50), self.color_blue, 1)
                image = cv2.putText(image, 'New Keypoint', (1000, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, self.color_green, 1, cv2.LINE_AA)
                image = cv2.rectangle(image, (990, 60), (1220, 100), self.color_green, 1)
        


        self.addButtonLocation(name='new_annotation', index=0, location=(990, 10, 1250, 50))
        self.addButtonLocation(name='new_keypoint', index=1, location=(990, 60, 1220, 100))

        if new_name != None:
            image = cv2.putText(image, 'New Name: ' + new_name, (1000, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_blue, 1, cv2.LINE_AA)

        image = cv2.putText(image, 'Keypoints', (700, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, self.color_blue, 1, cv2.LINE_AA)
        image = cv2.putText(image, 'Annotations', (400, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, self.color_blue, 1, cv2.LINE_AA)
        image = cv2.putText(image, 'Resolutions', (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, self.color_blue, 1, cv2.LINE_AA)
        
        image = cv2.putText(image, '1280x720',  (30, 150),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_blue, 1, cv2.LINE_AA)
        image = cv2.rectangle(image, (25, 130), (120, 160), self.color_blue, 1)
        self.addButtonLocation(name='resolution', resolution=(1280, 720), location=(25, 130, 120, 160))
        image = cv2.putText(image, '1600x900',  (30, 200),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_blue, 1, cv2.LINE_AA)
        image = cv2.rectangle(image, (25, 180), (120, 210), self.color_blue, 1)
        self.addButtonLocation(name='resolution', resolution=(1600, 900), location=(25, 180, 120, 210))
        image = cv2.putText(image, '1920x1080', (30, 250),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_blue, 1, cv2.LINE_AA)
        image = cv2.rectangle(image, (25, 230), (120, 260), self.color_blue, 1)
        self.addButtonLocation(name='resolution', resolution=(1920, 1080), location=(25, 230, 120, 260))
        image = cv2.putText(image, '3640x2060', (30, 300),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_blue, 1, cv2.LINE_AA)
        image = cv2.rectangle(image, (25, 280), (120, 310), self.color_blue, 1)
        self.addButtonLocation(name='resolution', resolution=(3640, 2060), location=(25, 280, 120, 310))



        for i, category in enumerate(all_categories):
   
            if selected_category == None:
                image = cv2.putText(image, category['name'], (700, 80 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_blue, 1, cv2.LINE_AA)
                image = cv2.rectangle(image, (695, 65 + i * 30), (800, 85 + i * 30), self.color_blue, 1)
            else:
                if selected_category['index'] ==  i:
                    image = cv2.putText(image, category['name'], (700, 80 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_green, 1, cv2.LINE_AA)
                    image = cv2.rectangle(image, (695, 65 + i * 30), (800, 85 + i * 30), self.color_green, 1)

                    for keypoint_index, keypoint in enumerate(category['keypoints']):
                        image = cv2.putText(image, keypoint, (400, 80 + keypoint_index * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_blue, 1, cv2.LINE_AA)

                else:
                    image = cv2.putText(image, category['name'], (700, 80 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_blue, 1, cv2.LINE_AA)
                    image = cv2.rectangle(image, (695, 65 + i * 30), (800, 85 + i * 30), self.color_blue, 1)

            self.addButtonLocation(name='annotation', index=i, location=(695, 65 + i * 30, 800, 85 + i * 30))



        return image, self.button_locations
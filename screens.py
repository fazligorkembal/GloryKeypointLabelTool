import cv2
import utils

class screen:
    def __init__(self):
        self.color_green = (0, 255, 0)
        self.color_red   = (0, 0, 255)
        self.color_blue  = (255, 0, 0)
        self.thickness = 1

    def annotation_screen(self, image, annotations = None, original_resolution=None,new_resolution=None, line_center=None, selected_point=None):
        image = cv2.putText(image, 'Annotation Screen', (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, self.color_blue, 2, cv2.LINE_AA)
        
        if line_center != None:
            image = cv2.line(image, (line_center[0], 0), (line_center[0], new_resolution[1]), self.color_green, self.thickness) 
            image = cv2.line(image, (0, line_center[1]), (new_resolution[0], line_center[1]), self.color_green, self.thickness) 
        
        if selected_point != None:
            image = cv2.circle(image, selected_point['location'], self.thickness, self.color_red, self.thickness)
            image = cv2.rectangle(image, selected_point['location'], line_center, self.color_red, self.thickness)
            
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
                image = cv2.circle(image, (xmin, ymin), self.thickness, self.color_green, self.thickness)
                image = cv2.circle(image, (xmax, ymax), self.thickness, self.color_green, self.thickness)


        return image


    def option_screen(self, image, selected_button=None, new_name=None, all_categories=None, selected_annotation=None):
        button_positions = []
        button_temp = {}

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
        



        button_temp['name']     = 'new_annotation'
        button_temp['index']    = 0
        button_temp['location'] = (990, 10, 1250, 50) 
        button_positions.append(button_temp)
        button_temp = {}


        button_temp['name']     = 'new_keypoint'
        button_temp['index']    = 1
        button_temp['location'] = (990, 60, 1220, 100)
        button_positions.append(button_temp)

        if new_name != None:
            image = cv2.putText(image, 'New Name: ' + new_name, (1000, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_blue, 1, cv2.LINE_AA)

        image = cv2.putText(image, 'Keypoints', (700, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, self.color_blue, 1, cv2.LINE_AA)
        image = cv2.putText(image, 'Annotations', (400, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, self.color_blue, 1, cv2.LINE_AA)


        for i, category in enumerate(all_categories):
            button_temp = {}
   
            if selected_annotation == None:
                image = cv2.putText(image, category['name'], (700, 80 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_blue, 1, cv2.LINE_AA)
                image = cv2.rectangle(image, (695, 65 + i * 30), (800, 85 + i * 30), self.color_blue, 1)
            else:
                if selected_annotation['index'] ==  i:
                    image = cv2.putText(image, category['name'], (700, 80 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_green, 1, cv2.LINE_AA)
                    image = cv2.rectangle(image, (695, 65 + i * 30), (800, 85 + i * 30), self.color_green, 1)

                    for keypoint_index, keypoint in enumerate(category['keypoints']):
                        image = cv2.putText(image, keypoint, (400, 80 + keypoint_index * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_blue, 1, cv2.LINE_AA)

                else:
                    image = cv2.putText(image, category['name'], (700, 80 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_blue, 1, cv2.LINE_AA)
                    image = cv2.rectangle(image, (695, 65 + i * 30), (800, 85 + i * 30), self.color_blue, 1)




            button_temp['name']     = 'annotation'
            button_temp['index']    = i
            button_temp['location'] =  (695, 65 + i * 30, 800, 85 + i * 30)
            button_positions.append(button_temp)



        return image, button_positions
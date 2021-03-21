import os
import math
def get_all_images(dataset_path):
    all_image_paths = []

    for dirname, subdirname, filenames in os.walk(dataset_path):
        for filename in filenames:
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('jpeg'):
                file_path = os.path.join(dirname, filename)
                all_image_paths.append(file_path)
    return all_image_paths


def reshapeToOriginalResolution(x, y, original_resolution, new_resolution):
    x = int((x / new_resolution[0]) * original_resolution[0])
    y = int((y / new_resolution[1]) * original_resolution[1])
    return x, y

def reshapeToNewResolution(x, y, original_resolution, new_resolution):
    x = int((x / original_resolution[0]) * new_resolution[0])
    y = int((y / original_resolution[1]) * new_resolution[1])
    return x, y

def getNearestPoint(selected_image_annotations, x, y, original_resolution, new_resolution):
    def getDistance(x1, y1, x2, y2):
        return math.sqrt( (x2 - x2) ** 2 + (y2 - y1) ** 2 )

    hold_distance = 10_000_000
    selected_point = {}
    x, y = reshapeToOriginalResolution(x, y, original_resolution, new_resolution)

    for index, annotation in enumerate(selected_image_annotations):
        bbox = annotation['bbox']
        xmin = bbox[0]
        ymin = bbox[1]
        xmax = bbox[0] + bbox[2]
        ymax = bbox[1] + bbox[3]

        temp_distance = getDistance(xmin,ymin, x, y)
        if temp_distance < hold_distance:
            hold_distance = temp_distance
            selected_point['point_name'] = 'xmin'
            selected_point['location'] = (xmin, ymin)
            selected_point['annotation_index'] = index
        
        temp_distance = getDistance(xmax, ymax, x, y)
        if temp_distance < hold_distance:
            hold_distance = temp_distance
            selected_point['point_name'] = 'xmax'
            selected_point['location'] = (xmax, ymax)
            selected_point['annotation_index'] = index
        

        axis_hold = []
        for axis_index, axis in enumerate(annotation['keypoints']):
            axis_hold.append(axis)
            if len(axis_hold) == 3:
                axis_x = axis_hold[0]
                axis_y = axis_hold[1]
                
                temp_distance = getDistance(axis_x, axis_y, x, y)
                if temp_distance < hold_distance:
                    hold_distance = temp_distance
                    selected_point['point_name'] = 'keypoint'
                    selected_point['location'] = (axis_x, axis_y)
                    selected_point['annotation_index'] = index
                axis_hold = []

    return hold_distance, selected_point

        


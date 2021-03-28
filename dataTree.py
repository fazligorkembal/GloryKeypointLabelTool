import json
import cv2
import os
class data:
    def __init__(self, json_path):
        self.data = {}
        self.json_path = json_path
        self.getData()

    def getData(self):
        try:
            with open(self.json_path) as f:
                data = json.load(f)
                self.data = data
        except:
            self.data['info'] = {}
            self.data['licenses'] = []
            self.data['categories'] = []
            self.data['images'] = []
            self.data['annotations'] = []

            self.addInfo('1', '2021', 'Keypoints', 'None', 'None', '2021')
            self.addlicense('1', 'None', 'None')

    def addInfo(self, year, version, description, contributor, url, date_created):
        dict_info = {}
        dict_info['year'] = year
        dict_info['version'] = version
        dict_info['description'] = description
        dict_info['contributor'] = contributor
        dict_info['url'] = url
        dict_info['date_created'] = date_created

        self.data['info'] = dict_info

    def addlicense(self, id_, url, name):
        new_license = {}
        new_license['id'] = id_
        new_license['url'] = url
        new_license['name'] = name

        self.data['licenses'].append(new_license)

    def addCategory(self, name, keypoints=None, skeleton=None):
        category = {}
        category['id'] = len(self.data['categories']) + 1
        category['name'] = name
        category['supercategory'] = name
        category['keypoints'] = []
        category['skeleton'] = []

        self.data['categories'].append(category)

    def addNewImage(self, image_path, original_resolution):
        temp_image = {}

        if len(self.data['images']) > 0:
            temp_image['id'] = self.data['images'][-1]['id'] + 1
        else:
            temp_image['id'] = 0

        temp_image['license'] = 1
        temp_image['file_name'] = image_path
        temp_image['height'] = original_resolution[0]
        temp_image['width']  = original_resolution[1]
        temp_image['date_captured'] = '2021'

        self.data['images'].append(temp_image)
        return temp_image

    def GetImageData(self, image_path, original_resolution):
        selected_image_data = None
        
        for image in self.data['images']:
            if image['file_name'] == image_path:
                selected_image_data = image
                break
        
        if selected_image_data == None:
            selected_image_data = self.addNewImage(image_path, original_resolution)
        
        return selected_image_data, self.getAnnotations(selected_image_data['id'])

    def getAnnotations(self, image_id):
        selected_annotations = []
        for annotation in self.data['annotations']:
            if image_id == annotation['image_id']:
                selected_annotations.append(annotation)
        return selected_annotations

    def addKeypointToCategoriesWithCategoryIndex(self, index, keypoint_name):
        self.data['categories'][index]['keypoints'].append(keypoint_name)

    def addAnnotationWithImageID(self, category_index, image_id, original_resolution, bbox, selected_image_annotations):
        temp_annotation = {}
        temp_annotation['id'] = len(selected_image_annotations)
        temp_annotation['image_id'] = image_id
        temp_annotation['category_id'] = self.data['categories'][category_index]['id']
        temp_annotation['segmentation'] = []
        temp_annotation['area'] = original_resolution[0] * original_resolution[1]
        temp_annotation['bbox'] = list(bbox)
        temp_annotation['iscrowd'] = 0
        temp_annotation['keypoints'] = []
        temp_annotation['num_keypoints'] = 0

        self.data['annotations'].append(temp_annotation)
        selected_image_annotations.append(temp_annotation)

        return selected_image_annotations

    def addKeypoint(self, selected_image_annotations, x, y, visible):
        
        selected_image_annotations[-1]['keypoints'].append(x)
        selected_image_annotations[-1]['keypoints'].append(y)
        selected_image_annotations[-1]['keypoints'].append(visible)

        num_keypoints = 0

        for index, axis in enumerate(selected_image_annotations[-1]['keypoints']):
            if index % 3 == 2 and axis == 2:
                num_keypoints += 1
        
        selected_image_annotations[-1]['num_keypoints'] = num_keypoints
        return selected_image_annotations

    def deleteAnnotation(self, annotation):
        self.data['annotations'].remove(annotation)

    def save(self):
        with open(self.json_path, 'w') as f:
            f.writelines(json.dumps(self.data, indent=4))


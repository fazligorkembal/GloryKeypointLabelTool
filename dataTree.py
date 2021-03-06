import json
import cv2

class data:

    def __init__(self, json_path):
        self.data = {}
        self.json_path = json_path

        self.getData()
        self.setAllAnnotationJsonIndexesToImages()


    def getData(self):
        try:
            with open(self.json_path) as f:
                data = json.load(f)
                self.data = data
                print("Dataset Found")

        except:
            print("Data Empty ... !")
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
        print("New Info is Added ... ")


    def addlicense(self, id_, url, name):
        new_license = {}
        new_license['id'] = id_
        new_license['url'] = url
        new_license['name'] = name

        self.data['licenses'].append(new_license)
        print("New License is Added ... ")


    def addCategory(self, name, supercategory, keypoints=[], skeleton=[]):
        category = {}
        category['id'] = len(self.data['categories'] + 1)
        category['name'] = name
        category['supercategory'] = supercategory
        category['keypoints'] = keypoints
        category['skeleton'] = skeleton

        self.data['categories'].append(category)
        print("New Category is Added ... ")


    def addImage(self, image_path):

        image = cv2.imread(image_path)
        height, width, channel = image.shape

        image_info = {}
        image_info['id'] = self.getNewImageId()
        image_info['license'] = 1
        image_info['file_name'] = image_path
        image_info['height'] = height
        image_info['width'] = width
        image_info['date_captured'] = '2021'
        image_info['annotation_json_indexes'] = []
        self.data['images'].append(image_info)
        print("New Image Added")
        return image_info['id']


    def addAnnotationWithImageJsonIndex(self, image_json_index, bbox, category_name):
        annotation = {}
        image = self.data['images'][image_json_index]
        annotation['id'] = len(image['annotation_json_indexes'])
        annotation['image_id'] = image['id']  
        annotation['category_id'] = self.getCategoryIdWithName(category_name)
        annotation['segmentation'] = []
        annotation['area'] = image['height'] * image['width']
        annotation['bbox'] = bbox
        annotation['iscrowd'] = 0
        
        image['annotation_json_indexes'].append(len(self.data['annotations']))
        self.data['annotations'].append(annotation)
        return (len(self.data['annotations']) - 1)


    def getImageAnnotationsWithImageIndex(self, image_json_index):
        image = self.data['images'][image_json_index]
        annotations = []
        for annotation_json_index in image['annotation_json_indexes']:
            annotations.append(self.data['annotations'][annotation_json_index])
        return annotations

    def getImageIndex(self, image_path):
        for index, image in enumerate(self.data['images']):
            if image_path == image['file_name']:
                return index
        self.addImage(image_path)
        return (len(self.data['images']) - 1)


    def getImageIndexes(self, image_paths):
        image_indexes = []
        for image_path in image_paths:
            image_indexes.append(self.getImageIndex(image_path))
        return image_indexes


    def getNewImageId(self):
        id_ = len(self.data['images'])
        return id_


    def getCategoryIdWithName(self, category_name):
        for category in self.data['categories']:
            if category['name'] == category_name:
                return category['id']


    def setAllAnnotationJsonIndexesToImages(self):
        for index, image in enumerate(self.data['images']):
            image['annotation_json_indexes'] = []
            
            for json_index, annotation in enumerate(self.data['annotations']):
                if image['id'] == annotation['image_id']:
                     annotation['image_id'] = index
                     image['annotation_json_indexes'].append(json_index)
            image['id'] = index

    def save(self):
        with open(self.json_path, 'w') as f:
            f.writelines(json.dumps(self.data, indent=4))


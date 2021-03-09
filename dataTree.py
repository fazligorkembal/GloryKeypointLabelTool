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


    def addCategory(self, name, keypoints=None, skeleton=None):
        category = {}
        category['id'] = len(self.data['categories']) + 1
        category['name'] = name
        category['supercategory'] = name
        category['keypoints'] = []
        category['skeleton'] = []

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
        image_info['annotation_indexes'] = []
        self.data['images'].append(image_info)
        print("New Image Added")
        return image_info['id']


    def addAnnotationWithImageIndex(self, image_index, bbox, category_index):
        annotation = {}
        image = self.data['images'][image_index]
        annotation['id'] = len(image['annotation_indexes'])
        annotation['image_id'] = image['id']  
        annotation['category_id'] = self.data['categories'][category_index]['id']
        annotation['segmentation'] = []
        annotation['area'] = image['height'] * image['width']
        annotation['bbox'] = bbox
        annotation['iscrowd'] = 0
        annotation['keypoints'] = []
        annotation['num_keypoints'] = 0
        image['annotation_indexes'].append(len(self.data['annotations']))
        
        self.data['annotations'].append(annotation)
        print("Annotation added ...")
        print(image)
        return annotation['id']

    def addKeypointToCategoriesWithCategoryIndex(self, index, keypoint_name):
        self.data['categories'][index]['keypoints'].append(keypoint_name)


    def getAnnotationsWithImageIndex(self, image_index):


        image = self.data['images'][image_index]

        
        annotations = []
        for annotation_index in image['annotation_indexes']:
            annotations.append(self.data['annotations'][annotation_index])
        return annotations


    def addKeypoint(self, annotation_index, x, y, visible, num_keypoints):
        print("num_keypoints")
        print(num_keypoints)
        print("annotation")
        print(self.data['annotations'][annotation_index])

        self.data['annotations'][annotation_index]['keypoints'].append(x)
        self.data['annotations'][annotation_index]['keypoints'].append(y)
        self.data['annotations'][annotation_index]['keypoints'].append(visible)
        self.data['annotations'][annotation_index]['num_keypoints'] = num_keypoints
        print("Keypoint added ... ")
        print(self.data['annotations'][annotation_index])

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
            image['annotation_indexes'] = []
            
            for json_index, annotation in enumerate(self.data['annotations']):
                if image['id'] == annotation['image_id']:
                     annotation['image_id'] = index
                     image['annotation_indexes'].append(json_index)
            image['id'] = index

    def save(self):
        with open(self.json_path, 'w') as f:
            f.writelines(json.dumps(self.data, indent=4))


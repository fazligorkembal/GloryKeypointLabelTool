import os

def get_all_images(dataset_path):
    all_image_paths = []

    for dirname, subdirname, filenames in os.walk(dataset_path):
        for filename in filenames:
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('jpeg'):
                file_path = os.path.join(dirname, filename)
                all_image_paths.append(file_path)
    return all_image_paths


def reshapeOriginalSizes(x, y, original_resolution, new_resolution):
    x = int((x / new_resolution[0]) * original_resolution[0])
    y = int((y / new_resolution[1]) * original_resolution[1])
    return x, y


def reshapeResizeSizes(x, y, original_resolution, new_resolution):
    x = int((x / original_resolution[0]) * new_resolution[0])
    y = int((y / original_resolution[1]) * new_resolution[1])
    return x, y
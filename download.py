'''
This script downloads TACO's images from Flickr given an annotation json file
Code written by Pedro F. Proenza, 2019
'''

import os.path
import argparse
import json
from PIL import Image
import requests
from io import BytesIO
import sys
import numpy as np
# import cv2
# import pandas as pd
# from PIL import Image
from pathlib import Path
# from tqdm import tqdm
# from utils import *


# Convert Coco bb to Yolo
def coco_to_yolo(x1, y1, w, h, image_w, image_h):
    return [((2*x1 + w)/(2*image_w)) , ((2*y1 + h)/(2*image_h)), w/image_w, h/image_h]

def coco91_to_coco80_class():  # converts 80-index (val2014) to 91-index (paper)
    """Converts COCO 91-class index (paper) to 80-class index (2014 challenge)."""
    return [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        None,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        None,
        24,
        25,
        None,
        None,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        None,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        58,
        59,
        None,
        60,
        None,
        None,
        61,
        None,
        62,
        63,
        64,
        65,
        66,
        67,
        68,
        69,
        70,
        71,
        72,
        None,
        73,
        74,
        75,
        76,
        77,
        78,
        79,
        None,
    ]

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--dataset_path', required=False, default= 'C:/CodeProjects/Trash Detection/data/annotations.json', help='Path to annotations')
    args = parser.parse_args()

    dataset_dir = os.path.dirname(args.dataset_path)

    print('Note. If for any reason the connection is broken. Just call me again and I will start where I left.')
    
    fn = Path(dataset_dir) / "labels"
    fn.mkdir(exist_ok=True, parents=True) # Ensure parent directories exist
        
    # Load annotations
    with open(args.dataset_path, 'r') as f:
        annotations = json.loads(f.read())
        coco80 = coco91_to_coco80_class()
        
        nr_images = len(annotations['images'])
        bboxes = []

        for k in range(len(annotations['annotations'])):
            datum = annotations['annotations'][k]
            # The COCO box format is [top left x, top left y, width, height]
            box = np.array(datum['bbox'], dtype=np.float64)

            # cls = coco80[datum["category_id"] - 1] # class
            # box = [cls] + box.tolist()
            # Testing if cls is needed
            box = [datum["category_id"]] + box.tolist()
            
            if box not in bboxes:
                    bboxes.append(box)

        for i in range(nr_images):

            image = annotations['images'][i]

            file_name = image['file_name']
            url_original = image['flickr_url']
            url_resized = image['flickr_640_url']

            file_path = os.path.join(dataset_dir, file_name)

            # Create subdir if necessary
            subdir = os.path.dirname(file_path)
            if not os.path.isdir(subdir):
                os.mkdir(subdir)

                

            if not os.path.isfile(file_path):
                # Load and Save Image
                response = requests.get(url_original)
                img = Image.open(BytesIO(response.content))
                if img._getexif():
                    img.save(file_path, exif=img.info["exif"])
                else:
                    img.save(file_path)

            # Show loading bar
            bar_size = 30
            x = int(bar_size * i / nr_images)
            sys.stdout.write("%s[%s%s] - %i/%i\r" % ('Loading: ', "=" * x, "." * (bar_size - x), i+1, nr_images))
            sys.stdout.flush()
            file_name = file_name[file_name.rfind('/')+1:]
            with open((fn / file_name).with_suffix(".txt"), "a") as file:
                for j in range(len(bboxes)):
                    if annotations['annotations'][j]['image_id'] == i:
                    
                        box = np.array(bboxes[j], dtype=np.float64)
                        file.write(str(int(box[0])) + " " + " ".join(str(element) for element in coco_to_yolo(box[1],box[2],box[3],box[4],image['width'],image['height'])) + "\n")
            i+=1
            
        sys.stdout.write('Finished\n')



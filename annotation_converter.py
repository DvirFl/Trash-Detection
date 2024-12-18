import json
import os
from ultralytics import YOLO
import argparse
import numpy as np
import random
import copy

def convert_coco_to_yolo(dataset_path, coco_annotation_path, yolo_annotation_path, image_dir):
    """Converts COCO annotations to YOLO format."""
    with open(dataset_path, 'r') as f:
        coco_annotations = json.load(f)

    yolo_annotations = []
    for annotation in coco_annotations['annotations']:
        image_id = annotation['image_id']
        category_id = annotation['category_id']
        bbox = annotation['bbox']  # [x_min, y_min, width, height]
        x_center = (bbox[0] + bbox[2] / 2) / coco_annotations['images'][image_id -1]['width']
        y_center = (bbox[1] + bbox[3] / 2) / coco_annotations['images'][image_id -1]['height']
        width = bbox[2] / coco_annotations['images'][image_id -1]['width']
        height = bbox[3] / coco_annotations['images'][image_id -1]['height']
        yolo_annotations.append([image_id -1, x_center, y_center, width, height, category_id -1])

    with open(yolo_annotation_path, 'w') as f:
        json.dump(yolo_annotations, f)

    # Create labels.txt
    labels = set()
    for annotation in coco_annotations['annotations']:
        labels.add(annotation['category_id'])
    with open(os.path.join(image_dir, 'labels.txt'), 'w') as f:
        for label in sorted(list(labels)):
            f.write(str(label -1) + '\n')

def split_dataset(dataset_path, test_percentage=15, val_percentage=15, nr_trials=10):
    with open(dataset_path, 'r') as f:
        dataset = json.load(f)

    anns = dataset['annotations']
    scene_anns = dataset['scene_annotations']
    imgs = dataset['images']
    nr_images = len(imgs)

    nr_testing_images = int(nr_images * test_percentage * 0.01 + 0.5)
    nr_nontraining_images = int(nr_images * (test_percentage + val_percentage) * 0.01 + 0.5)

    for i in range(nr_trials):
        random.shuffle(imgs)

        train_set = {
            'info': None,
            'images': [],
            'annotations': [],
            'scene_annotations': [],
            'licenses': [],
            'categories': [],
            'scene_categories': [],
        }
        train_set['info'] = dataset['info']
        train_set['categories'] = dataset['categories']
        train_set['scene_categories'] = dataset['scene_categories']

        val_set = copy.deepcopy(train_set)
        test_set = copy.deepcopy(train_set)

        test_set['images'] = imgs[0:nr_testing_images]
        val_set['images'] = imgs[nr_testing_images:nr_nontraining_images]
        train_set['images'] = imgs[nr_nontraining_images:nr_images]

        test_img_ids, val_img_ids, train_img_ids = [], [], []
        for img in test_set['images']:
            test_img_ids.append(img['id'])

        for img in val_set['images']:
            val_img_ids.append(img['id'])

        for img in train_set['images']:
            train_img_ids.append(img['id'])

        for ann in anns:
            if ann['image_id'] in test_img_ids:
                test_set['annotations'].append(ann)
            elif ann['image_id'] in val_img_ids:
                val_set['annotations'].append(ann)
            elif ann['image_id'] in train_img_ids:
                train_set['annotations'].append(ann)

        for ann in scene_anns:
            if ann['image_id'] in test_img_ids:
                test_set['scene_annotations'].append(ann)
            elif ann['image_id'] in val_img_ids:
                val_set['scene_annotations'].append(ann)
            elif ann['image_id'] in train_img_ids:
                train_set['scene_annotations'].append(ann)

        ann_train_out_path = f'data/annotations_{i}_train.json'
        ann_val_out_path = f'data/annotations_{i}_val.json'
        ann_test_out_path = f'data/annotations_{i}_test.json'

        os.makedirs('data', exist_ok=True)

        with open(ann_train_out_path, 'w+') as f:
            json.dump(train_set, f)

        with open(ann_val_out_path, 'w+') as f:
            json.dump(val_set, f)

        with open(ann_test_out_path, 'w+') as f:
            json.dump(test_set, f)

        image_dir = 'data/images'
        os.makedirs(image_dir, exist_ok=True)
        convert_coco_to_yolo(dataset_path,ann_train_out_path, f'{image_dir}/train_{i}.json', image_dir)
        convert_coco_to_yolo(dataset_path,ann_val_out_path, f'{image_dir}/val_{i}.json', image_dir)
        convert_coco_to_yolo(dataset_path,ann_test_out_path, f'{image_dir}/test_{i}.json', image_dir)


# Example usage:
split_dataset('data/annotations.json')

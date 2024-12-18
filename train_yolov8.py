import cv2
import ultralytics
from ultralytics import YOLO
import json
import logging
import os
import split_dataset as split
import shutil
from pathlib import Path
import sys
import yaml
import numpy as np

def copy_files(filename_list, image_dest, label_dest):
    with open(filename_list, 'r') as f:
        for line in f:
            jpg_source, txt_source = line.strip().split()
            jpg_source = jpg_source.replace('/','\\')
            txt_source = txt_source.replace('/','\\')
            head, sep, jpg_file_name = jpg_source.split('\\')
            head, sep, txt_file_name = txt_source.split('\\')
            # jpg_source = os.path.join('data', jpg_source)
            # txt_source = os.path.join('data', txt_source)
            jpg_destination = os.path.join(image_dest, jpg_file_name)
            txt_destination = os.path.join(label_dest, txt_file_name)

            try:
                shutil.copy2(jpg_source, jpg_destination)
                shutil.copy2(txt_source, txt_destination)
                # print(f"Copied {jpg_source} to {jpg_destination} and {txt_source} to {txt_destination}")
            except FileNotFoundError:
                print(f"Error: File not found: {jpg_source} or {txt_source}")
            except Exception as e:
                print(f"An error occurred: {e}")

path = r"C:\CodeProjects\Trash Detection\data"

# This is a very dangerous line!!!
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

if False:
    try:
        folders = ['train', 'val', 'test']
        subfolders = ['images', 'labels']
        for folder in folders:
            folder_path = os.path.join(path, folder)
            os.makedirs(folder_path, exist_ok=True)
            for subfolder in subfolders:
                subfolder_path = os.path.join(folder_path, subfolder)
                os.makedirs(subfolder_path, exist_ok=True)
                [f.unlink() for f in Path(subfolder_path).glob("*") if f.is_file()] 

        image_dir = "data/images"
        label_dir = "data/labels"
        split.split_dataset(image_dir, label_dir)
        copy_files(filename_list=os.path.join(path,'train.txt'),image_dest=os.path.join(path,'train/images'),label_dest=os.path.join(path,'train/labels'))
        copy_files(filename_list=os.path.join(path,'validate.txt'),image_dest=os.path.join(path,'val/images'),label_dest=os.path.join(path,'val/labels'))
        copy_files(filename_list=os.path.join(path,'test.txt'),image_dest=os.path.join(path,'test/images'),label_dest=os.path.join(path,'test/labels'))
    except OSError as e:
        print(f"Error creating folders and splitting data: {e}")


# Configure logging
logging.basicConfig(filename='training_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load a model
try:
    model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.exception(f"Error loading model: {e}")

# Load data.yaml to get train and val paths
with open(os.path.join(path, "data.yaml"), 'r') as f:
    data_yaml = yaml.safe_load(f)
train_path = os.path.join(path, data_yaml['train'])
val_path = os.path.join(path, data_yaml['val'])

# Test image loading
image_files = [f for f in os.listdir(train_path) if f.endswith(('.jpg', '.jpeg', '.png'))][:5]
for image_file in image_files:
    try:
        image_path = os.path.join(train_path, image_file)
        im = cv2.imread(image_path)
        if im is None:
            logging.error(f"cv2.imread failed to load image: {image_path}")
        else:
            logging.info(f"cv2.imread loaded image: {image_path}")
    except Exception as e:
        logging.exception(f"Error loading image with cv2.imread: {image_path}, {e}")


# Train the model
try:
    results = model.train(data=os.path.join(path,"data.yaml"), epochs=300, imgsz=640)
    logging.info("Training completed successfully.")
except Exception as e:
    logging.exception(f"Error during training: {e}")
    sys.exit() 

# Validate the model
try:
    results = model.val(data=val_path, imgsz=640)
    logging.info("Validation completed successfully.")
except Exception as e:
    logging.exception(f"Error during validation: {e}")
    sys.exit() 

# Test the model and get the results
try:
    test_image_path = 'data/images/000001.jpg'
    if os.path.exists(test_image_path):
        results = model.predict(source=test_image_path, conf=0.5)
        logging.info("Prediction completed successfully.")
    else:
        logging.error(f"Test image not found: {test_image_path}")
        results = None
except Exception as e:
    logging.exception(f"Error during prediction: {e}")

# Save results to a JSON file
try:
    if results:
        with open('results.json', 'w') as f:
            json.dump(results, f, indent=4)
        logging.info("Results saved to results.json")
    else:
        logging.warning("No results to save.")
except Exception as e:
    logging.exception(f"Error saving results: {e}")

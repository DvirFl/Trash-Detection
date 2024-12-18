import os
import shutil

def copy_files(filename_list, image_dest, label_dest):
    with open(filename_list, 'r') as f:
        for line in f:
            jpg_file, txt_file = line.strip().split()
            jpg_source = os.path.join('data', jpg_file)
            txt_source = os.path.join('data', txt_file)
            jpg_destination = os.path.join(image_dest, jpg_file)
            txt_destination = os.path.join(label_dest, txt_file)

            try:
                shutil.copy2(jpg_source, jpg_destination)
                shutil.copy2(txt_source, txt_destination)
                print(f"Copied {jpg_source} to {jpg_destination} and {txt_source} to {txt_destination}")
            except FileNotFoundError:
                print(f"Error: File not found: {jpg_source} or {txt_source}")
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    filename_list = "data/test.txt"
    image_destination = "data/test/images"
    label_destination = "data/test/labels"
    copy_files(filename_list, image_destination, label_destination)

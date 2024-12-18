import os
import random
import shutil

def split_dataset(image_dir, label_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    """Splits a dataset into train, validation, and test sets.

    Args:
        image_dir: Path to the directory containing images.
        label_dir: Path to the directory containing labels.
        train_ratio: Ratio of images for the training set.
        val_ratio: Ratio of images for the validation set.
        test_ratio: Ratio of images for the test set.
    """

    image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    num_images = len(image_files)

    num_train = int(num_images * train_ratio)
    num_val = int(num_images * val_ratio)
    num_test = num_images - num_train - num_val

    random.shuffle(image_files)

    train_images = image_files[:num_train]
    val_images = image_files[num_train:num_train + num_val]
    test_images = image_files[num_train + num_val:]

    def write_split(split_name, image_list):
        with open(f"{split_name}.txt", "w") as f:
            for img_file in image_list:
                img_path = os.path.join(image_dir, img_file)
                label_path = os.path.join(label_dir, img_file.replace(".jpg", ".txt")) # Assuming labels are .txt
                f.write(f"{img_path} {label_path}\n")

    write_split("train", train_images)
    write_split("validate", val_images)
    write_split("test", test_images)


if __name__ == "__main__":
    image_dir = "data/images"
    label_dir = "data/labels"
    split_dataset(image_dir, label_dir)

import json
import os

def modify_json_data(data, object_key):
    """Pads numeric values in the specified object to six digits.

    Args:
        data: The JSON data (dictionary).
        object_key: The key of the object to modify.

    Returns:
        The modified JSON data, or None if an error occurs.
    """
    try:
        if 'images' not in data:
            print(f"Error: Object key 'images' not found in JSON data.")
            return None

        # if object_key not in data:
        #     print(f"Error: Object key '{object_key}' not found in JSON data.")
        #     return None

        obj = data['images']
        for idx, item in enumerate(obj):
            if object_key in item:
                # item = dict.fromkeys(item)
                item['file_name'] = "images/{:06d}".format(int(idx)) + ".jpg"
                obj[idx] = item
        
        # if not isinstance(obj, dict):
        #     print(f"Error: Object '{object_key}' is not a dictionary.")
        #     return None

        # for key, value in obj.items():
        #     if isinstance(value, (int, float)):
        #         obj[key] = "{:06d}".format(int(value))  # Pad to 6 digits

        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def modify_json_file(file_path="C:\\CodeProjects\\Trash Detection\\data\\annotations.json", object_key="file_name"):
    """Modifies a JSON file by padding numeric values.

    Args:
        file_path: Path to the JSON file.
        object_key: Key of the object to modify.

    Returns:
        True if successful, False otherwise.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return False

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        modified_data = modify_json_data(data, object_key)
        if modified_data:
            with open(file_path, 'w') as f:
                json.dump(modified_data, f, indent=4)
            return True
        else:
            return False
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


if __name__ == "__main__":
    # file_path = input("Enter the path to the JSON file: ")
    # object_key = "file_name"  # Fixed object key
    # if modify_json_file(file_path, object_key):
    if modify_json_file(file_path="C:\\CodeProjects\\Trash Detection\\data\\annotations.json", object_key="file_name"):
        print("JSON file modified successfully")
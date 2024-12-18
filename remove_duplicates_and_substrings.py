import re

def remove_duplicates(text):
    words = text.split()
    unique_words = []
    for word in words:
        if word not in unique_words:
            unique_words.append(word)
    return " ".join(unique_words)

def remove_substrings(text, substrings):
    for substring in substrings:
        text = text.replace(substring, "")
    return text

def process_text(text, substrings):
    text = remove_duplicates(text)
    text = remove_substrings(text, substrings)
    return text

# Example usage
text = '[{"supercategory": "Aluminium foil", "id": 0, "name": "Aluminium foil"}, {"supercategory": "Battery", "id": 1, "name": "Battery"}, {"supercategory": "Blister pack", "id": 2, "name": "Aluminium blister pack"}, {"supercategory": "Blister pack", "id": 3, "name": "Carded blister pack"}, {"supercategory": "Bottle", "id": 4, "name": "Other plastic bottle"}, {"supercategory": "Bottle", "id": 5, "name": "Clear plastic bottle"}, {"supercategory": "Bottle", "id": 6, "name": "Glass bottle"}, {"supercategory": "Bottle cap", "id": 7, "name": "Plastic bottle cap"}, {"supercategory": "Bottle cap", "id": 8, "name": "Metal bottle cap"}, {"supercategory": "Broken glass", "id": 9, "name": "Broken glass"}, {"supercategory": "Can", "id": 10, "name": "Food Can"}, {"supercategory": "Can", "id": 11, "name": "Aerosol"}, {"supercategory": "Can", "id": 12, "name": "Drink can"}, {"supercategory": "Carton", "id": 13, "name": "Toilet tube"}, {"supercategory": "Carton", "id": 14, "name": "Other carton"}, {"supercategory": "Carton", "id": 15, "name": "Egg carton"}, {"supercategory": "Carton", "id": 16, "name": "Drink carton"}, {"supercategory": "Carton", "id": 17, "name": "Corrugated carton"}, {"supercategory": "Carton", "id": 18, "name": "Meal carton"}, {"supercategory": "Carton", "id": 19, "name": "Pizza box"}, {"supercategory": "Cup", "id": 20, "name": "Paper cup"}, {"supercategory": "Cup", "id": 21, "name": "Disposable plastic cup"}, {"supercategory": "Cup", "id": 22, "name": "Foam cup"}, {"supercategory": "Cup", "id": 23, "name": "Glass cup"}, {"supercategory": "Cup", "id": 24, "name": "Other plastic cup"}, {"supercategory": "Food waste", "id": 25, "name": "Food waste"}, {"supercategory": "Glass jar", "id": 26, "name": "Glass jar"}, {"supercategory": "Lid", "id": 27, "name": "Plastic lid"}, {"supercategory": "Lid", "id": 28, "name": "Metal lid"}, {"supercategory": "Other plastic", "id": 29, "name": "Other plastic"}, {"supercategory": "Paper", "id": 30, "name": "Magazine paper"}, {"supercategory": "Paper", "id": 31, "name": "Tissues"}, {"supercategory": "Paper", "id": 32, "name": "Wrapping paper"}, {"supercategory": "Paper", "id": 33, "name": "Normal paper"}, {"supercategory": "Paper bag", "id": 34, "name": "Paper bag"}, {"supercategory": "Paper bag", "id": 35, "name": "Plastified paper bag"}, {"supercategory": "Plastic bag & wrapper", "id": 36, "name": "Plastic film"}, {"supercategory": "Plastic bag & wrapper", "id": 37, "name": "Six pack rings"}, {"supercategory": "Plastic bag & wrapper", "id": 38, "name": "Garbage bag"}, {"supercategory": "Plastic bag & wrapper", "id": 39, "name": "Other plastic wrapper"}, {"supercategory": "Plastic bag & wrapper", "id": 40, "name": "Single-use carrier bag"}, {"supercategory": "Plastic bag & wrapper", "id": 41, "name": "Polypropylene bag"}, {"supercategory": "Plastic bag & wrapper", "id": 42, "name": "Crisp packet"}, {"supercategory": "Plastic container", "id": 43, "name": "Spread tub"}, {"supercategory": "Plastic container", "id": 44, "name": "Tupperware"}, {"supercategory": "Plastic container", "id": 45, "name": "Disposable food container"}, {"supercategory": "Plastic container", "id": 46, "name": "Foam food container"}, {"supercategory": "Plastic container", "id": 47, "name": "Other plastic container"}, {"supercategory": "Plastic glooves", "id": 48, "name": "Plastic glooves"}, {"supercategory": "Plastic utensils", "id": 49, "name": "Plastic utensils"}, {"supercategory": "Pop tab", "id": 50, "name": "Pop tab"}, {"supercategory": "Rope & strings", "id": 51, "name": "Rope & strings"}, {"supercategory": "Scrap metal", "id": 52, "name": "Scrap metal"}, {"supercategory": "Shoe", "id": 53, "name": "Shoe"}, {"supercategory": "Squeezable tube", "id": 54, "name": "Squeezable tube"}, {"supercategory": "Straw", "id": 55, "name": "Plastic straw"}, {"supercategory": "Straw", "id": 56, "name": "Paper straw"}, {"supercategory": "Styrofoam piece", "id": 57, "name": "Styrofoam piece"}, {"supercategory": "Unlabeled litter", "id": 58, "name": "Unlabeled litter"}, {"supercategory": "Cigarette", "id": 59, "name": "Cigarette"}], "scene_categories": [{"id": 0, "name": "Clean"}, {"id": 1, "name": "Indoor, Man-made"}, {"id": 2, "name": "Pavement"}, {"id": 3, "name": "Sand, Dirt, Pebbles"}, {"id": 4, "name": "Trash"}, {"id": 5, "name": "Vegetation"}, {"id": 6, "name": "Water"}]}'
substrings_to_remove = ["supercategory", ",", ":","{","}","[","]","\"","1","2","3","4","5","6","7","8","9","0","id","name"]
processed_text = process_text(text, substrings_to_remove)
print(f"Original text: {text}")
print(f"Processed text: {processed_text}")

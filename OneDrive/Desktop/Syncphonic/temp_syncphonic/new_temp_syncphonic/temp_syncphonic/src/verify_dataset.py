print("Verification script started...")  # Initial debug statement

import os
import pandas as pd
import cv2

def verify_captions_file(file_path):
    print("Starting captions file verification...")  # Debug statement
    if not os.path.exists(file_path):
        print(f"Captions file does not exist: {file_path}")
        return
    try:
        captions_df = pd.read_csv(file_path)
        print("Captions file loaded successfully.")
        print("First few rows of the captions file:")
        print(captions_df.head())
        
        # Check for expected columns
        expected_columns = ['image_name', 'comment']
        if all(column in captions_df.columns for column in expected_columns):
            print("Captions file has the expected columns.")
        else:
            print("Captions file is missing some expected columns.")
            print("Found columns:", captions_df.columns)
            print("Expected columns:", expected_columns)
    except Exception as e:
        print(f"Error loading captions file: {e}")

def verify_images_directory(dir_path):
    print("Starting images directory verification...")  # Debug statement
    if not os.path.exists(dir_path):
        print(f"Images directory does not exist: {dir_path}")
        return
    
    image_files = os.listdir(dir_path)
    if not image_files:
        print(f"No images found in the directory: {dir_path}")
        return
    
    print(f"Found {len(image_files)} images in the directory.")
    print("First few images:", image_files[:5])
    
    # Try loading a few images
    for image_file in image_files[:5]:
        image_path = os.path.join(dir_path, image_file)
        try:
            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to load image: {image_file}")
            else:
                print(f"Successfully loaded image: {image_file}")
        except Exception as e:
            print(f"Error loading image {image_file}: {e}")

def main():
    print("Verification script is running...")  # Debug statement
    caption_file = 'C:/Users/sreec/OneDrive/Desktop/Syncphonic/data/flickr30k_images/results.csv'
    image_dir = 'C:/Users/sreec/OneDrive/Desktop/Syncphonic/data/flickr30k_images/flickr30k_images'

    print("Verifying captions file...")
    verify_captions_file(caption_file)

    print("\nVerifying images directory...")
    verify_images_directory(image_dir)

if __name__ == "__main__":
    main()

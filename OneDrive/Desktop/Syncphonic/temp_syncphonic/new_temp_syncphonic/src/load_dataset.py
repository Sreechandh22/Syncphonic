import os
import pandas as pd
import cv2
import numpy as np

def load_captions(captions_file):
    captions_df = pd.read_csv(captions_file)
    print("Captions file loaded successfully.")
    return captions_df

def load_images(image_dir, sample_size=None):
    image_files = os.listdir(image_dir)
    if sample_size:
        image_files = image_files[:sample_size]

    images = []
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        image = cv2.imread(image_path)
        if image is not None:
            images.append((image_file, image))
        else:
            print(f"Failed to load image: {image_file}")
    
    print(f"Loaded {len(images)} images from {image_dir}")
    return images

def main():
    captions_file = 'C:/Users/sreec/OneDrive/Desktop/Syncphonic/data/flickr30k_images/results.csv'
    image_dir = 'C:/Users/sreec/OneDrive/Desktop/Syncphonic/data/flickr30k_images/flickr30k_images'
    
    print("Loading captions...")
    captions = load_captions(captions_file)
    
    print("Loading images...")
    images = load_images(image_dir, sample_size=30)  # Adjust sample size if needed
    
    # Save or return data for further processing
    return captions, images

if __name__ == "__main__":
    main()

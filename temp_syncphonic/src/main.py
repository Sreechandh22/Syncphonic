import logging
import os
import pandas as pd
import sys
import torch
import clip
from PIL import Image
os.environ['TF_MLIR_ENABLE_V1_COMPILER'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_MLIR_ENABLE_V1_COMPILER'] = '1'

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from src.data_preprocessing import load_images, load_captions, get_vocab, convert_captions_to_sparse
from src.train_model import train_model, predict_caption
from src.clip_caption_generator import load_clip_model, generate_caption
from src.mood_detection import load_mood_detection_model, detect_mood
from src.music_mapping import map_mood_to_music
from src.sentiment_analysis import load_sentiment_analysis_model, analyze_sentiment

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    print("Starting main script...")  # Debug statement
    logging.info("Starting main script...")
    
    image_dir = 'C:/Users/sreec/OneDrive/Desktop/Syncphonic/data/flickr30k_images/flickr30k_images'
    caption_file = 'C:/Users/sreec/OneDrive/Desktop/Syncphonic/data/flickr30k_images/results.csv'

    # Verify the dataset is downloaded and extracted correctly
    if not os.path.exists(image_dir):
        print(f"Image directory not found: {image_dir}")  # Debug statement
        logging.error("Image directory not found: %s", image_dir)
        return
    if not os.path.exists(caption_file):
        print(f"Caption file not found: {caption_file}")  # Debug statement
        logging.error("Caption file not found: %s", caption_file)
        return
    print("Verified dataset files exist.")  # Debug statement
    logging.info("Verified dataset files exist.")

    logging.info("Loading image names from captions file...")
    try:
        captions_df = pd.read_csv(caption_file)
        image_names = captions_df['image_name'].unique().tolist()
        logging.debug(f"Image names: {image_names[:5]}... (total {len(image_names)})")
        print(f"Found {len(image_names)} unique image names in captions file.")  # Debug statement
    except Exception as e:
        print(f"Error in loading image names: {e}")  # Debug statement
        logging.error("Error in loading image names: %s", e)
        return
    logging.info(f"Found {len(image_names)} unique image names in captions file.")

    logging.info("Loading images...")
    try:
        train, real_images, image_names = load_images(image_dir, image_names)
        print(f"Loaded {len(train)} images.")  # Debug statement
    except Exception as e:
        print(f"Error in loading images: {e}")  # Debug statement
        logging.error("Error in loading images: %s", e)
        return
    logging.info(f"Loaded {len(train)} images.")

    logging.info("Loading captions...")
    try:
        captions = load_captions(caption_file, image_names)
        print(f"Loaded {len(captions)} captions.")  # Debug statement
    except Exception as e:
        print(f"Error in loading captions: {e}")  # Debug statement
        logging.error("Error in loading captions: %s", e)
        return
    logging.info(f"Loaded {len(captions)} captions.")

    logging.info("Building vocabulary...")
    try:
        vocab_size, sentences, fwd_dict, rev_dict = get_vocab(captions)
        print(f"Vocabulary size: {vocab_size}")  # Debug statement
    except Exception as e:
        print(f"Error in building vocabulary: {e}")  # Debug statement
        logging.error("Error in building vocabulary: %s", e)
        return
    logging.info(f"Vocabulary size: {vocab_size}")

    logging.info("Converting captions to sparse matrices...")
    try:
        train_captions = convert_captions_to_sparse(sentences, vocab_size, fwd_dict)
        print("Conversion to sparse matrices completed.")  # Debug statement
    except Exception as e:
        print(f"Error in converting captions to sparse matrices: {e}")  # Debug statement
        logging.error("Error in converting captions to sparse matrices: %s", e)
        return
    logging.info("Conversion completed.")

    logging.info("Training model...")
    try:
        sess = train_model(train, train_captions, vocab_size, fwd_dict)
        print("Model training completed.")  # Debug statement
    except Exception as e:
        print(f"Error in training model: {e}")  # Debug statement
        logging.error("Error in training model: %s", e)
        return
    logging.info("Model training completed.")

    logging.info("Predicting captions...")
    try:
        predict_caption(sess, train, real_images, train_captions, vocab_size, rev_dict)
        print("Caption prediction completed.")  # Debug statement
    except Exception as e:
        print(f"Error in predicting captions: {e}")  # Debug statement
        logging.error("Error in predicting captions: %s", e)
        return
    logging.info("Prediction completed.")
 
    # Additional steps for CLIP caption generation, mood detection, and sentiment analysis
    logging.info("Loading CLIP model...")
    try:
        clip_model, clip_preprocess, clip_device = load_clip_model()
        print("CLIP model loaded.")  # Debug statement
    except Exception as e:
        print(f"Error in loading CLIP model: {e}")  # Debug statement
        logging.error("Error in loading CLIP model: %s", e)
        return
    logging.info("CLIP model loaded.")

    for image_name in image_names[:5]:  # Example: processing first 5 images
        image_path = f"{image_dir}/{image_name}"
        
        # Get all captions for the image
        candidate_texts = captions_df[captions_df['image_name'] == image_name]['comment'].tolist()
        
        logging.info(f"Generating caption for {image_path}...")
        try:
            caption = generate_caption(clip_model, clip_preprocess, clip_device, image_path, candidate_texts)
            print(f"Generated Caption for {image_path}: {caption}")  # Debug statement
        except Exception as e:
            print(f"Error in generating caption for {image_path}: {e}")  # Debug statement
            logging.error("Error in generating caption: %s", e)
            continue
        logging.info(f"Generated Caption: {caption}")

        logging.info("Loading mood detection model...")
        try:
            mood_model, mood_device = load_mood_detection_model()
            print("Mood detection model loaded.")  # Debug statement
        except Exception as e:
            print(f"Error in loading mood detection model: {e}")  # Debug statement
            logging.error("Error in loading mood detection model: %s", e)
            continue
        logging.info("Mood detection model loaded.")

        logging.info(f"Detecting mood for {image_path}...")
        try:
            mood = detect_mood(mood_model, mood_device, caption)
            print(f"Detected Mood for {image_path}: {mood}")  # Debug statement
        except Exception as e:
            print(f"Error in detecting mood for {image_path}: {e}")  # Debug statement
            logging.error("Error in detecting mood: %s", e)
            continue
        logging.info(f"Detected Mood: {mood}")

        logging.info("Mapping mood to music...")
        try:
            music_track = map_mood_to_music(mood)
            print(f"Mapped Music Track for {mood}: {music_track}")  # Debug statement
        except Exception as e:
            print(f"Error in mapping mood to music for {mood}: {e}")  # Debug statement
            logging.error("Error in mapping mood to music: %s", e)
            continue
        logging.info(f"Mapped Music Track: {music_track}")

        logging.info("Loading sentiment analysis model...")
        try:
            sentiment_analysis = load_sentiment_analysis_model()
            print("Sentiment analysis model loaded.")  # Debug statement
        except Exception as e:
            print(f"Error in loading sentiment analysis model: {e}")  # Debug statement
            logging.error("Error in loading sentiment analysis model: %s", e)
            continue
        logging.info("Sentiment analysis model loaded.")

        logging.info(f"Analyzing sentiment for caption: {caption}...")
        try:
            sentiment = analyze_sentiment(sentiment_analysis, caption)
            print(f"Sentiment Analysis Result for caption: {sentiment}")  # Debug statement
        except Exception as e:
            print(f"Error in analyzing sentiment for caption: {e}")  # Debug statement
            logging.error("Error in analyzing sentiment: %s", e)
            continue
        logging.info(f"Sentiment Analysis Result: {sentiment}")

if __name__ == "__main__":
    main()

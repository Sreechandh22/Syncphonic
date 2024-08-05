import os
import cv2
import numpy as np
import pandas as pd
import re
from scipy.sparse import csr_matrix, vstack

def load_images(image_dir, image_names):
    train = []
    real_images = []
    for img_name in image_names:
        img_path = os.path.join(image_dir, img_name)
        img = cv2.imread(img_path)
        if img is not None:
            real_images.append(img)
            img_resized = cv2.resize(img, (256, 256))
            train.append(img_resized.reshape(1, 256, 256, 3))
    train = np.vstack(train)
    return train, real_images, image_names

def load_captions(caption_file, image_names):
    try:
        captions_df = pd.read_csv(caption_file)
        if set(['image_name', 'comment_number', 'comment']).issubset(captions_df.columns):
            captions_df = captions_df[['image_name', 'comment']]
            captions_df = captions_df.groupby('image_name')['comment'].apply(list).reset_index()
            captions = []
            for img_name in image_names:
                img_captions = captions_df[captions_df['image_name'] == img_name]['comment'].tolist()
                captions.append(' '.join(img_captions[0]))
            return captions
        else:
            raise ValueError("The captions file does not contain the required columns: 'image_name', 'comment_number', 'comment'")
    except Exception as e:
        print(f"Error in loading captions: {e}")
        return None

def get_vocab(captions):
    start_tag = '<s>'
    end_tag = '<e>'
    arr = []
    sentences = []
    for caption in captions:
        caption = re.sub(' +', ' ', caption)
        sentence = start_tag + ' ' + caption + ' ' + end_tag
        sentences.append(sentence.split())
        arr.extend(sentence.split())
    arr = list(set(arr))
    vocab_size = len(arr)
    fwd_dict = {word: idx for idx, word in enumerate(arr)}
    rev_dict = {idx: word for idx, word in enumerate(arr)}
    return vocab_size, sentences, fwd_dict, rev_dict

def convert_captions_to_sparse(sentences, vocab_size, fwd_dict):
    train_caption = []
    for sentence in sentences:
        cap_array = None
        for word in sentence:
            row = [0]
            col = [fwd_dict[word]]
            data = [1]
            if cap_array is None:
                cap_array = csr_matrix((data, (row, col)), shape=(1, vocab_size))
            else:
                cap_array = vstack((cap_array, csr_matrix((data, (row, col)), shape=(1, vocab_size))))
        train_caption.append(cap_array)
    return train_caption

import unittest
from src.data_preprocessing import load_images, load_captions, get_vocab, convert_captions_to_sparse

class TestDataPreprocessing(unittest.TestCase):
    
    def test_load_images(self):
        image_dir = '../data/flickr30k_images/flickr30k_images/'
        train, real_images, image_names = load_images(image_dir)
        self.assertEqual(len(train), 30)
        self.assertEqual(len(real_images), 30)
        self.assertEqual(len(image_names), 30)

    def test_load_captions(self):
        caption_file = '../data/flickr30k_images/results.csv'
        image_names = ['1000092795.jpg']
        captions = load_captions(caption_file, image_names)
        self.assertEqual(len(captions), 1)

    def test_get_vocab(self):
        captions = ["This is a test caption."]
        vocab_size, sentences, fwd_dict, rev_dict = get_vocab(captions)
        self.assertGreater(vocab_size, 0)
        self.assertGreater(len(sentences), 0)
        self.assertGreater(len(fwd_dict), 0)
        self.assertGreater(len(rev_dict), 0)

    def test_convert_captions_to_sparse(self):
        captions = ["This is a test caption."]
        vocab_size, sentences, fwd_dict, rev_dict = get_vocab(captions)
        train_captions = convert_captions_to_sparse(sentences, vocab_size, fwd_dict)
        self.assertEqual(len(train_captions), 1)
        
if __name__ == "__main__":
    unittest.main()

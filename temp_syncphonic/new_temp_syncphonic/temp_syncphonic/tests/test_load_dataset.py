import unittest
from src.load_dataset import download_and_extract_kaggle

class TestLoadDataset(unittest.TestCase):
    
    def test_download_and_extract(self):
        test_dataset = "hsankesara/image-captioning"
        test_extract_to = "./test_data/"
        
        # Run download and extract function
        download_and_extract_kaggle(test_dataset, extract_to=test_extract_to)
        
        # Check if the data is extracted correctly
        self.assertTrue(os.path.exists(test_extract_to))
        self.assertTrue(len(os.listdir(test_extract_to)) > 0)
        
        # Cleanup
        for file in os.listdir(test_extract_to):
            os.remove(os.path.join(test_extract_to, file))
        os.rmdir(test_extract_to)

if __name__ == "__main__":
    unittest.main()

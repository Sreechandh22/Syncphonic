from transformers import BertTokenizer, BertForSequenceClassification
import torch

def load_mood_detection_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = BertForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    tokenizer = BertTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model.to(device)
    return model, tokenizer, device

def detect_mood(model, tokenizer, device, text):
    inputs = tokenizer(text, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = outputs.logits.softmax(dim=-1).cpu().numpy()
    return probs

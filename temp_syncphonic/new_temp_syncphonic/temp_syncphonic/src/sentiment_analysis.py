from transformers import pipeline

def load_sentiment_analysis_model():
    sentiment_analysis = pipeline("sentiment-analysis")
    return sentiment_analysis

def analyze_sentiment(sentiment_analysis, text):
    result = sentiment_analysis(text)[0]
    return result

# Example usage
if __name__ == "__main__":
    sentiment_analysis = load_sentiment_analysis_model()
    text = "This is a test caption."
    sentiment = analyze_sentiment(sentiment_analysis, text)
    print("Sentiment Analysis Result:", sentiment)

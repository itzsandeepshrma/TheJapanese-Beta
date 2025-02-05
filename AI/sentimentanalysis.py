from textblob import TextBlob

class SentimentAnalysis:
    def __init__(self):
        pass

    def analyze_sentiment(self, text):
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        if polarity > 0:
            return "Positive"
        elif polarity == 0:
            return "Neutral"
        else:
            return "Negative"

# Example usage
sentiment_analyzer = SentimentAnalysis()
print(sentiment_analyzer.analyze_sentiment("I love this bot!"))

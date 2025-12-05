# message_analyzer.py
from langdetect import detect, DetectorFactory, LangDetectException
from textblob import TextBlob

DetectorFactory.seed = 42  # makes results consistent across runs

class MessageAnalyzer:
    def __init__(self):
        pass

    def detect_language(self, text: str) -> str:
        try:
            if not text or len(text.strip()) < 5:
                return "en"  # fallback for very short inputs
            return detect(text)
        except LangDetectException:
            return "en"  # fallback if detection fails
        except Exception:
            return "en"

    def analyze_sentiment(self, text: str) -> str:
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            if polarity > 0.2:
                return "positive"
            elif polarity < -0.2:
                return "negative"
            else:
                return "neutral"
        except Exception:
            return "neutral"

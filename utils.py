import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from nltk.sentiment import SentimentIntensityAnalyzer
from gtts import gTTS

# ✅ News Extraction (Improved for Bing News)
def get_news(company_name):
    url = f"https://www.bing.com/news/search?q={company_name}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for item in soup.select("a[href^='http']")[:10]:  # Updated selector
        title = item.text.strip() if item.text else "No title available"
        link = item["href"] if "href" in item.attrs else "#"
        articles.append({"title": title, "link": link})

    return articles

# ✅ Summarization
def summarize_text(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 2)  # Extract 2 key sentences
    return " ".join(str(sentence) for sentence in summary)

# ✅ Sentiment Analysis
def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)
    return "Positive" if score["compound"] > 0 else "Negative" if score["compound"] < 0 else "Neutral"

# ✅ Comparative Sentiment Analysis
def comparative_analysis(articles):
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment = analyze_sentiment(article['summary'])
        sentiment_counts[sentiment] += 1

    return sentiment_counts

# ✅ Text-to-Speech (TTS)
def text_to_speech(text, filename="output.mp3"):
    tts = gTTS(text, lang='hi')
    tts.save(filename)
    return filename

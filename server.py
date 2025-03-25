import nltk
import os

# Explicitly set NLTK data path
nltk.data.path.append("C:\\Users\\Harshith\\AppData\\Roaming\\nltk_data")

from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import get_news, summarize_text, analyze_sentiment, comparative_analysis, text_to_speech

app = Flask(__name__)
CORS(app)  # Allow frontend access


@app.route("/news", methods=["GET"])
def fetch_news():
    company = request.args.get("company")
    if not company:
        return jsonify({"error": "Company name is required"}), 400

    articles = get_news(company)
    if not articles:
        return jsonify({"error": "No news articles found"}), 404

    return jsonify({"articles": articles}), 200


@app.route("/sentiment", methods=["GET"])
def fetch_sentiment():
    company = request.args.get("company")
    if not company:
        return jsonify({"error": "Company name is required"}), 400

    articles = get_news(company)
    print(f"Fetched {len(articles)} articles for {company}")  # Debugging log

    if not articles:
        return jsonify({"error": "No articles found for sentiment analysis"}), 404

    summaries = []
    for article in articles:
        title = article.get("title", "No title available")
        summary = summarize_text(title) if title else "No summary available"
        summaries.append({"title": title, "summary": summary})

    print(f"Generated {len(summaries)} summaries")  # Debugging log

    if not summaries:
        return jsonify({"error": "No summaries generated"}), 500

    #Apply `analyze_sentiment` to each summary
    sentiment_results = [
        {"title": s["title"], "sentiment": analyze_sentiment(s["summary"])}
        for s in summaries
    ]

    print(f"Individual Sentiment Analysis: {sentiment_results}")  # Debugging log

    #Perform comparative analysis on all summaries
    sentiments = comparative_analysis(summaries)

    print(f"Overall Sentiment Distribution: {sentiments}")  # Debugging log

    response_data = {
        "individual_sentiments": sentiment_results,
        "overall_sentiments": sentiments,
    }

    return jsonify(response_data), 200


@app.route("/tts", methods=["GET"])
def generate_tts():
    company = request.args.get("company")
    if not company:
        return jsonify({"error": "Company name is required"}), 400

    summary_text = f"{company} has been analyzed. The sentiment is available."
    filename = text_to_speech(summary_text)

    return jsonify({"audio_file": filename}), 200


if __name__ == "__main__":
    app.run(debug=True)

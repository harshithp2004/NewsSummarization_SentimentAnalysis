import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:5000"

st.title("News Summarization & Sentiment Analysis")

company_name = st.text_input("Enter a company name:")
if st.button("Analyze"):
    if not company_name.strip():
        st.error("Please enter a valid company name.")
    else:
        # Fetch news articles
        news_response = requests.get(f"{BASE_URL}/news", params={"company": company_name})
        if news_response.status_code == 200:
            articles = news_response.json().get("articles", [])
            if articles:
                st.write("###Summarized News")
                for article in articles:
                    title = article.get("title", "No title available")
                    link = article.get("link", "#")
                    st.write(f"🔹 **{title}** - [Read More]({link})")
            else:
                st.warning("No articles found for this company.")
        else:
            st.error(f"Failed to fetch news: {news_response.json().get('error', 'Unknown error')}")

        # Fetch sentiment analysis
        sentiment_response = requests.get(f"{BASE_URL}/sentiment", params={"company": company_name})


        st.write("Raw Sentiment Response:", sentiment_response.text)

        if sentiment_response.status_code == 200:
            try:
                response_json = sentiment_response.json()
                individual_sentiments = response_json.get("individual_sentiments", [])
                overall_sentiments = response_json.get("overall_sentiments", {})

                # Display Individual Sentiments
                if individual_sentiments:
                    st.write("###Individual Sentiment Analysis")
                    st.json(individual_sentiments)

                # Display Overall Sentiments
                if overall_sentiments:
                    st.write("###Overall Sentiment Distribution")
                    st.json(overall_sentiments)
                else:
                    st.warning("No overall sentiment analysis available.")

            except requests.exceptions.JSONDecodeError:
                st.error("Failed to parse JSON from the server.")
        else:
            st.error(f"API Error: {sentiment_response.status_code} - {sentiment_response.text}")

        # Generate TTS (only if summaries exist)
        summary_text = " ".join([article.get("title", "") for article in articles if article.get("title")])
        if summary_text:
            tts_response = requests.get(f"{BASE_URL}/tts", params={"company": company_name})
            if tts_response.status_code == 200:
                st.write("###Audio Summary")
                st.audio("output.mp3")
            else:
                st.error(f"Failed to generate TTS: {tts_response.json().get('error', 'Unknown error')}")
        else:
            st.warning("No valid summary available for TTS.")

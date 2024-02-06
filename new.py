import json
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

# Download NLTK resources (stopwords and punkt tokenizer)
import nltk
nltk.download('stopwords')
nltk.download('punkt')

def load_articles_from_json(file_path='bbc_articles.json'):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            articles = json.load(json_file)
        return articles
    except FileNotFoundError:
        return []

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    # Remove punctuation and convert to lowercase
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    # Tokenize the text and remove stopwords
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(filtered_tokens)

def cluster_articles(articles):
    # Extract title for clustering and preprocess
    content = [preprocess_text(article['title']) for article in articles]

    # Vectorize the content using TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(content)

    # Cluster the articles using K-Means
    num_clusters = 6
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    clusters = kmeans.fit_predict(X)

    # Assign clusters to articles
    for i, article in enumerate(articles):
        article['cluster'] = clusters[i]

    return articles

def main():
    st.title("News Clustering with Streamlit - BBC News")

    # Load articles from the JSON file
    bbc_articles = load_articles_from_json()

    if not bbc_articles:
        st.warning("No news articles available. Make sure to run the scraper to fetch and store articles.")
        return

    st.subheader("BBC News Articles:")
    for article in bbc_articles:
        st.write(f"[{article['title']}]({article['link']}) - {article['description']}")

    # Cluster articles
    clustered_articles = cluster_articles(bbc_articles)

    # Display clustered articles
    st.subheader("Clustered News:")
    for cluster_id in range(max(clustered_articles, key=lambda x: x['cluster'])['cluster'] + 1):
        st.subheader(f"Cluster {cluster_id + 1}")
        for article in clustered_articles:
            if article['cluster'] == cluster_id:
                st.write(f"[{article['title']}]({article['link']}) - {article['description']}")

if __name__ == "__main__":
    main()

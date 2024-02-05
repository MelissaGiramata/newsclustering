import streamlit as st
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def get_bbc_news_articles():
    url = 'https://www.bbc.com/news/world'
    response = requests.get(url)

    if response.status_code != 200:
        st.error(f"Failed to fetch news articles from BBC News. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup( response.text, 'html.parser')

    # Extract news articles
    articles = []
    for article in soup.find_all('div', class_='gs-c-promo'):
        title = article.find('h3', class_='gs-c-promo-heading__title').text.strip()
        
        # Check if the 'a' tag is found before accessing its attributes
        link_tag = article.find('a', class_='gs-c-promo-heading')
        if link_tag:
            link = url + link_tag.get('href', '').strip()
        else:
            link = ''
        
        # Check if the 'p' tag is found before accessing its text attribute
        description_tag = article.find('p', class_='gs-c-promo-summary')
        description = description_tag.text.strip() if description_tag else ''
        
        content = f"{title} {description}"  # Concatenate title and description for content
        articles.append({'title': title, 'link': link, 'description': description, 'content': content})

    return articles

def cluster_articles(articles):
    # Extract content for clustering
    content = [article['content'] for article in articles]

    # Vectorize the content using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(content)

    # Cluster the articles using K-Means
    num_clusters = 3  # You can adjust the number of clusters
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    clusters = kmeans.fit_predict(X)

    # Assign clusters to articles
    for i, article in enumerate(articles):
        article['cluster'] = clusters[i]

    return articles

def main():
    st.title("News Clustering with Streamlit - BBC News")

    # Fetch and display news articles
    bbc_articles = get_bbc_news_articles()

    if not bbc_articles:
        st.warning("No news articles available.")
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

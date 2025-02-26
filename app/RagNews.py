from dotenv import load_dotenv
import os

# Newspaper3k
from newspaper import Article
from newspaper import ArticleException

import chromadb
from langchain_openai.embeddings import OpenAIEmbeddings

import hashlib
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("Api key for openai is missing")

print(f"Using openai api:{openai_api_key[:5]}******")

from TextSummarizer import TextSummarizer

class RagNews:
    def __init__(self):
        self.summarizer = TextSummarizer()
        # Vector database
        self.collection = chromadb.PersistentClient("./news_db").get_or_create_collection("query_news")
        
        # Initializing the OpenAI embeddings
        self.embedding_model = OpenAIEmbeddings(openai_api_key=openai_api_key)

    def extract_full_content(self, url):
        """Extracts the full news content from the given URL."""
        article = Article(url)
        article.download()
        try:
            article.parse()
            return f"{article.title}\n{article.text}"
        except ArticleException:
            return None

    def summarize_headlines(self, articles):
        """Summarizes news headlines from multiple articles."""
        extracted_articles = []
        for article in articles:
            content = self.extract_full_content(article["url"])
            if content is not None:
                extracted_articles.append(content)
        return self.summarizer.summarize(extracted_articles, "news headlines")

    def summarize_query(self, articles, query, user_input):
        """Retrieves relevant articles and generates a summary based on user query."""
        relevant_articles = self.retrieve_relevant_articles(articles, query)
        return self.summarizer.summarize(relevant_articles[0], user_input)

    def vectorize_articles(self, articles):
        """Populates the vector database with news embeddings."""
        for article in articles:
            content = self.extract_full_content(article["url"])
            if content:
                embedding = self.embedding_model.embed_query(content)
                hash_id = hashlib.md5(content.encode()).hexdigest()
                self.collection.upsert(
                    ids=[hash_id],
                    embeddings=[embedding],
                    documents=[content]
                )

    def retrieve_relevant_articles(self, articles, query):
        """Retrieves top 10 relevant articles from the vector database based on the query."""
        self.vectorize_articles(articles)
        query_embedding = self.embedding_model.embed_query(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=10
        )
        return results["documents"]

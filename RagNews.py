from dotenv import load_dotenv
import os

# Newspaper3k
from newspaper import Article
from newspaper import ArticleException

import chromadb
from langchain_openai.embeddings import OpenAIEmbeddings

import hashlib
load_dotenv()

from Summarizer import Summariser
class RagNews:

  def __init__(self):

    self.summariser = Summariser()
    # Vector database
    self.collection = chromadb.PersistentClient("./news_db").get_or_create_collection("query_news")

    # Intilising the Openai embeddings
    self.embedding_model = OpenAIEmbeddings(openai_api_key = os.getenv("openai"))


  def extract_full_content(self,url):
    # Extracting full News content
    article = Article(url)
    article.download()
    try:
      article.parse()
      return article.title + "\n" + article.text
    except ArticleException:
      return None

  def headline_summariser(self, articles):
    extracted_articles = []
    for article in articles:
      content =self.extract_full_content(article["url"])
      if content != None:
        extracted_articles.append(content)
    return self.summariser.summary(extracted_articles, "news headlines")

  # Retrieval augmented generation #

  def query_summariser(self, articles, query, user_input):
    relevant_articles = self.retrieve_relevant_articles(articles, query)
    return self.summariser.summary(relevant_articles[0], user_input)


  def vectorisation(self, articles):
    # Populating the vector database with news embeddings
    for index, article in enumerate(articles):
      content = self.extract_full_content(article["url"])
      if content != None:
        embedding = self.embedding_model.embed_query(content)
        hash_id = hashlib.md5(content.encode()).hexdigest()
        self.collection.upsert(
          ids = [hash_id],
          embeddings = [embedding],
          documents = [content]
      )

  def retrieve_relevant_articles(self, articles, query):
    # Vector data base
    self.vectorisation(articles)

    query_embedding = self.embedding_model.embed_query(query)
    # Retrieval of news articles related to given query
    results = self.collection.query(
        query_embeddings = [query_embedding],
        n_results = 10) # top 10 related articles
    return results["documents"]
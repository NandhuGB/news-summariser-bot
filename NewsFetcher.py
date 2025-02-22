# OOPS
from abc import ABC, abstractmethod
# API
from newsapi import NewsApiClient
# Common
import os
from dotenv import load_dotenv

load_dotenv()

# News fetcher factory design setup
class NewsFetcher(ABC):
  @abstractmethod
  def fetch(self, input:dict):
    pass
    
# Factory Newsapi-python
class NewsApiFetcher(NewsFetcher):
  """
  Fetching news using newsapi-python
  1. Headline
    Input:
          q - query
          category - general, sports, business, technology, ..
          language - 2 character language code "en"
          country - 2 character country code "us"

    Return:

  """
  def __init__(self):
    # Intialising the client
    self.client = NewsApiClient(api_key = os.getenv("newsapi-py"))
    self.country = "us"
    self.language = "en"

  def fetch(self, input):

    if input["type"] =="headline":     # Fetching headline - 15 articles
      try:
        articles = self.client.get_top_headlines(q = "",language = self.language, country = self.country)["articles"]
        return self.refactor(articles[:15])
      except:
        return None

    elif input["type"]=="query":      # Fetching related news
      try:
        articles = self.client.get_everything(q = input["query"], language = input["language"], sort_by = "relevancy")["articles"]
        return self.refactor(articles)
      except:
        return None

  def refactor(self, articles):
    """Refactoring the api result"""
    # Handling empty result
    length= len(articles)
    if length == 0:
      return None
    elif length > 20: # limiting number of output to 20
      length = 20

    # Refactoring all the news
    result = []
    for article in articles[:length]:
      result.append({"title":article["title"],"url":article["url"]})
    return result
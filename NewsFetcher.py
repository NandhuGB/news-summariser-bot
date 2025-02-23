from abc import ABC, abstractmethod
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

class NewsFetcher(ABC):
    """
    Abstract base class for fetching news.
    """
    @abstractmethod
    def fetch(self, params: dict):
        pass

class NewsApiFetcher(NewsFetcher):
    """
    Fetches news articles using the News API.
    """
    def __init__(self):
        self.client = NewsApiClient(api_key=os.getenv("NEWSAPI_KEY"))
        self.default_country = "us"
        self.default_language = "en"

    def fetch(self, params: dict):
        """
        Fetches news based on the provided parameters.
        
        Args:
            params (dict): Contains query parameters for the API.
        
        Returns:
            list: A list of formatted news articles (title, url) or None if no results.
        """
        try:
            if params.get("type") == "headline":
                articles = self.client.get_top_headlines(
                    q=params.get("query", ""),
                    language=self.default_language,
                    country=self.default_country
                )["articles"]
            elif params.get("type") == "query":
                articles = self.client.get_everything(
                    q=params.get("query"),
                    language=params.get("language", self.default_language),
                    sort_by="relevancy"
                )["articles"]
            else:
                return None
            
            return self._format_articles(articles)
        except Exception as e:
            print(f"Error fetching news: {e}")
            return None

    def _format_articles(self, articles: list):
        """
        Formats the news articles by extracting title and URL.
        
        Args:
            articles (list): List of articles returned from the API.
        
        Returns:
            list: A list of dictionaries with "title" and "url" (max 15 articles).
        """
        if not articles:
            return None
        
        formatted_articles = [
            {"title": article["title"], "url": article["url"]}
            for article in articles[:15]
        ]
        return formatted_articles


## For debugging ##
    # def command(self, command_type: str, query: str = "", language: str = "en"):
    #     """
    #     Executes a command to fetch news articles.
        
    #     Args:
    #         command_type (str): Type of news to fetch ("headline" or "query").
    #         query (str, optional): Search term for news. Defaults to "".
    #         language (str, optional): Language for news. Defaults to "en".
        
    #     Returns:
    #         list: Formatted news articles or None.
    #     """
    #     params = {"type": command_type, "query": query, "language": language}
    #     return self.fetch(params)

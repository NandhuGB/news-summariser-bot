from NewsFetcher import NewsApiFetcher
from RagNews import RagNews

from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

class NewsBotMediator:
    def __init__(self):
        """Initializes the NewsBotMediator with necessary components."""
        self.news_fetcher = NewsApiFetcher()  # News fetcher
        self.rag_news = RagNews()  # Retrieval-augmented generation
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # OpenAI client

    def fetch_headlines(self):
        """Fetches and summarizes top news headlines."""
        articles = self.news_fetcher.fetch({"type": "headline", "query":""})
        
        if not articles:
            return "No results found."
        
        return self.rag_news.summarize_headlines(articles)

    def fetch_query_based_news(self, user_input):
        """Fetches and summarizes news based on user query."""
        extracted_parameters = self.extract_news_parameters(user_input)
        articles = self.news_fetcher.fetch(extracted_parameters)
        return self.rag_news.summarize_query(articles, extracted_parameters["rag_keywords"], user_input)

    def extract_news_parameters(self, user_input):
        """Extracts and returns optimized search parameters for NewsAPI's `get_everything` method."""
        system_prompt = """Extract key variables from user input:
        - Query: Extract only the most relevant keywords (3-5) for an optimized NewsAPI search.
        - Country: Extract 2-letter ISO 3166-1 code if provided; else return "us".
        - Language: Extract 2-letter ISO-639-1 code if provided; else return "en".
        - RAG Keywords: Additional key terms useful for filtering fetched articles in a vector database.
        
        Format the query keywords with `AND` or `OR` where necessary to optimize NewsAPI search performance.
        
        Always return a valid JSON object:
        {
            "query": "AI AND robotics OR automation",
            "country": "us",
            "language": "en",
            "rag_keywords": "deep learning GPT models transformers"
        }
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0  # Ensures consistent structured output
            )
            
            response_text = response.choices[0].message.content
            parameters = json.loads(response_text)
            
            # Set default values if missing
            parameters.setdefault("country", "us")
            parameters.setdefault("language", "en")
            parameters.setdefault("type", "query")
            parameters.setdefault("rag_keywords", user_input)
            
            return parameters
        
        except (json.JSONDecodeError, AttributeError, IndexError) as e:
            print(f"Error parsing response: {e}")
            return {"query": user_input, "country": "us", "language": "en", "type": "query", "rag_keywords": user_input}

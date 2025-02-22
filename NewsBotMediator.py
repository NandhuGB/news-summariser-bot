from NewsFetcher import NewsApiFetcher
from RagNews import RagNews

from openai import OpenAI
from dotenv import load_dotenv
import os
import json
load_dotenv()


class NewsBotMediator():
  def __init__(self):
    self.newsapi = NewsApiFetcher()  # News fetcher
    self.rag = RagNews()             # Retrieval augmented generation
    self.client = OpenAI(api_key = os.getenv("openai")) # Openai client


  def headlines(self):

    # Fetching headlines
    articles = self.newsapi.fetch({"type":"headline"})

    # Hanlding empty return
    if articles == None:
      
      return "NO results found"
    # Summarising
    summary = self.rag.headline_summariser(articles)
    return summary

  def query(self, user_input):

    # Extracting parameters from user_input
    extracted_parameters = self.extract_news_parameters(user_input)
    # Fetching relevant articles
    articles = self.newsapi.fetch(extracted_parameters)
    summary = self.rag.query_summariser(articles, extracted_parameters["rag_keywords"], user_input)
    return summary


  def extract_news_parameters(self, user_input):
      """Extracts and returns optimized search parameters for NewsAPI get_everything method."""

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

          # Extract response content
          response_text = response.choices[0].message.content

          # Parse response JSON
          parameters = json.loads(response_text)

          # Set default values if missing
          parameters["country"] = parameters.get("country", "us")
          parameters["language"] = parameters.get("language", "en")
          parameters["type"] = parameters.get("type","query")
          parameters["rag_keywords"] = parameters.get("rag_keywords", user_input)

          return parameters

      except (json.JSONDecodeError, AttributeError, IndexError) as e:
          print(f"Error parsing response: {e}")
          return {"query": user_input, "country": "us", "language": "en", "type":"query", "rag_keywords":user_input}
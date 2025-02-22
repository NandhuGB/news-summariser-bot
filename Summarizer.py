# Imports
import os
from dotenv import load_dotenv
import tiktoken
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents.base import Document
from langchain.chains.summarize.chain import load_summarize_chain
load_dotenv()




class Summariser:

  def __init__(self):
    self.llm = ChatOpenAI(model = "gpt-3.5-turbo", temperature =0, api_key=os.getenv("openai"))


  # Sliding windows text splitter

  def split_text_sliding_window(self, text, chunk_size=16300, overlap=500):
      """Splits text into overlapping chunks using a sliding window approach."""
      splitter = RecursiveCharacterTextSplitter(
          chunk_size=chunk_size, chunk_overlap=overlap, separators=["\n\n", "\n", " "]
      )
      chunks = splitter.split_text(text)
      return [Document(page_content=chunk) for chunk in chunks]


  def summarize_chunks(self,chunks):
      """Summarizes each chunk individually."""
      chain = load_summarize_chain(self.llm, chain_type="map_reduce")  # Uses a MapReduce summarization approach
      summaries = [chain.run({"input_documents":[chunk]}) for chunk in chunks]
      return summaries

  def merge_summaries(self, summaries, user_query):
    """Generates a final coherent summary from chunk summaries."""

    final_prompt = (f"Summarize these summaries into a clear and concise final summary, "
                f"ensuring it is directly relevant to the following user query: '{user_query}'.\n"
                + "\n".join(summaries))



    response = self.llm.invoke(final_prompt)

    return response

  def summary(self, articles, user_query):
      """Full pipeline to summarize long text using a sliding window approach."""

      text = "\n".join(articles)


      # Total number of tokens
      no_of_tokens = len(tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text))

      if no_of_tokens < 16300:
        final_summary = self.merge_summaries(articles, user_query)
        return final_summary.content

      # If document exceeds models token limit

      # Step 1: Split text
      chunks = self.split_text_sliding_window(text)

      # Step 2: Summarize each chunk
      chunk_summaries = self.summarize_chunks(chunks)

      # Step 3: Merge chunk summaries into a final summary
      final_summary = self.merge_summaries(chunk_summaries, user_query)

      return final_summary.content
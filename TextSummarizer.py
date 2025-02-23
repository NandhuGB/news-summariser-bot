import os
from dotenv import load_dotenv
import tiktoken
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.chains.summarize import load_summarize_chain

load_dotenv()

class TextSummarizer:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

    def split_text(self, text, chunk_size=16300, overlap=500):
        """Splits text into overlapping chunks using a sliding window approach."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=overlap, separators=["\n\n", "\n", " "]
        )
        chunks = splitter.split_text(text)
        return [Document(page_content=chunk) for chunk in chunks]

    def summarize_chunks(self, chunks):
        """Summarizes each chunk individually."""
        chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        return [chain.run({"input_documents": [chunk]}) for chunk in chunks]

    def generate_final_summary(self, summaries, user_query):
        """Generates a final coherent summary from chunk summaries."""
        final_prompt = (
            f"Summarize these summaries into a clear and concise final summary, "
            f"ensuring it is directly relevant to the following user query: '{user_query}'.\n"
            + "\n".join(summaries)
        )
        return self.llm.invoke(final_prompt)

    def summarize(self, articles, user_query):
        """Full pipeline to summarize long text using a sliding window approach."""
        text = "\n".join(articles)
        token_count = len(tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text))
        
        # Direct summary for  input tokens less the 16300
        if token_count < 16300:
            return self.generate_final_summary(articles, user_query).content

        chunks = self.split_text(text)
        chunk_summaries = self.summarize_chunks(chunks)
        final_summary = self.generate_final_summary(chunk_summaries, user_query)
        
        return final_summary.content

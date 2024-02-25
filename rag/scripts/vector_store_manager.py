import os
import weaviate
from weaviate.embedded import EmbeddedOptions
from langchain.vectorstores import Weaviate, FAISS, Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv, find_dotenv
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

class VectorStoreManager:
    def __init__(self):
        
        # Load OpenAI API key from .env file
        load_dotenv(find_dotenv())
        self.openai_api_key = os.environ["OPENAI_API_KEY"]
        
        if self.openai_api_key is None:
            raise ValueError("OpenAI API key not found in environment variables.")
        
        # Initialize Weaviate client
        self.weaviate_client = weaviate.Client(embedded_options=EmbeddedOptions())
        
    def create_weaviate_vectorstore(self, chunks):
        try:
            # Populate vector database using OpenAIEmbeddings
            embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            vectorstore = Weaviate.from_documents(
                client=self.weaviate_client,
                documents=chunks,
                embedding=embedding_function,
                by_text=False
            )
            print("Weaviate vector store created successfully.")
            return vectorstore

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def create_faiss_vectorstore(self, chunks):
        try:

            embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            vectorstore = FAISS.from_documents(chunks, embedding_function)

            print("FAISS vector store created successfully.")
            return vectorstore

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def create_chroma_vectorstore(self, chunks):
        try:

            embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            vectorstore = Chroma.from_documents(chunks, embedding_function)

            print("Chroma vector store created successfully.")
            return vectorstore

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

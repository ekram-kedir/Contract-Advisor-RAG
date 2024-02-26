import logging
import os

from langchain.agents import tool
from pydantic import BaseModel, Field
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatCohere
from langchain_community.embeddings import CohereEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv


class SQLQuery(BaseModel):
    query: str = Field(description="SQL query to execute")  # Likely unused


load_dotenv()
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")


@tool
def qa_tool() -> RetrievalQA:
    """
    Creates and returns a RetrievalQA tool for knowledge retrieval interactions.

    This tool utilizes Cohere embeddings and a Chroma vector store to retrieve
    relevant information from a knowledge base for answering user questions.

    Raises:
        Exception: If an error occurs during tool creation.
    """

    logging.basicConfig(level=logging.INFO)  # Configure logging for potential errors

    try:

        cohere_embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)
        llm = ChatCohere(temperature=0.1, model="text-davinci-003")
        raw_documents = TextLoader("./../rag/prompts/context.txt").load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        documents = text_splitter.split_documents(raw_documents)
        db = Chroma.from_documents(documents, cohere_embeddings)
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",  # More descriptive chain type name
            retriever=db.as_retriever(),
        )
        return qa

    except Exception as e:
        logging.error(f"Error creating QA tool: {e}")
        raise Exception("Failed to create QA tool")


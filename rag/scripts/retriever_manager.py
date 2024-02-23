import os
import chromadb
from langchain.retrievers import (
    ParentDocumentRetriever,
    BM25Retriever,
    EnsembleRetriever,
    MultiQueryRetriever
)
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import FAISS

class RetrieverManager:
    def __init__(self):
        # Load OpenAI API key from .env file
        load_dotenv(find_dotenv())
        self.openai_api_key = os.environ.get("OPENAI_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not found in environment variables.")
        

    def create_parent_document_retriever(self, documents, query):
        try:
            parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
            child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
            
            vectorstore = chromadb(
    collection_name="split_parents", embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

)
            store = InMemoryStore()

            retriever = ParentDocumentRetriever(
                vectorstore=vectorstore,
                docstore=store,
                child_splitter=child_splitter,
                parent_splitter=parent_splitter
            )
            
            # Add documents
            retriever.add_documents(documents)
            print("Documents added successfully.")
            
            relevant_docs = retriever.get_relevant_documents(query)
            return retriever,relevant_docs

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def create_ensemble_retriever(self, doc_list1, doc_list2, query):
        try:
            bm25_retriever = BM25Retriever.from_texts(doc_list1, metadatas=[{"source": 1}] * len(doc_list1)
)
            bm25_retriever.k = 2

            embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            faiss_vectorstore = FAISS.from_texts(
            doc_list2, embedding_function, metadatas=[{"source": 2}] * len(doc_list2)
            )
            faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs={"k": 2})


            ensemble_retriever = EnsembleRetriever(
                retrievers=[bm25_retriever, faiss_retriever], weights=[0.5, 0.5]
            )
            
            # Add documents
            # ensemble_retriever.add_documents(documents)
            # print("Documents added successfully.")
            
            relevant_docs = ensemble_retriever.get_relevant_documents(query)
            return ensemble_retriever,relevant_docs
        

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def create_multi_query_retriever(self, vectorstore, query):
        try:
            llm = ChatOpenAI(temperature=0, openai_api_key=self.openai_api_key)
            retriever_from_llm = MultiQueryRetriever.from_llm(
                retriever=vectorstore.as_retriever(), llm=llm
            )
            
            relevant_docs = retriever_from_llm.get_relevant_documents(query)
            return retriever_from_llm, relevant_docs

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None



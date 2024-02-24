from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter  
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
import random

import weaviate
from dotenv import load_dotenv,find_dotenv
from weaviate.embedded import EmbeddedOptions

def data_loader(file_path= '../../rag/prompts/context.txt', chunk_size=500, chunk_overlap=50):
    try:
        loader = TextLoader(file_path)
        documents = loader.load()

        # Chunk the data
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents(documents)
        
        print("data loaded to vector database successfully")
        return chunks
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None 


def create_langchain_pipeline(retriever, template, temperature=0):
    try:
        # Define LLM
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=temperature)

        # Define prompt template
        
        prompt = ChatPromptTemplate.from_template(template)

        # Setup RAG pipeline
        rag_chain = (
            {"context": retriever,  "question": RunnablePassthrough()} 
            | prompt 
            | llm
            | StrOutputParser() 
        )

        print("langchain with rag pipeline created successfully.")
        return rag_chain

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None 
    

def create_retriever(chunks):
    try:
        
        # Load OpenAI API key from .env file
        load_dotenv(find_dotenv())


        # Setup vector database
        client = weaviate.Client(
            embedded_options = EmbeddedOptions()
        )

        # Populate vector database
        vectorstore = Weaviate.from_documents(
            client = client,    
            documents = chunks,
            embedding = OpenAIEmbeddings(),
            by_text = False
        )

        # Define vectorstore as retriever to enable semantic search
        retriever = vectorstore.as_retriever()
        print("create retriver  succesfully.")

        return retriever
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None 
    
def monte_carlo_eval(prompt):
    try:
        # Simulating different types of responses
        response_types = ['highly relevant', 'somewhat relevant', 'irrelevant']
        scores = {'highly relevant': 3, 'somewhat relevant': 2, 'irrelevant': 1}

        # Perform multiple random trials
        trials = 100
        total_score = 0
        for _ in range(trials):
            response = random.choice(response_types)
            total_score += scores[response]

        # Average score represents the evaluation
        return total_score / trials
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None 

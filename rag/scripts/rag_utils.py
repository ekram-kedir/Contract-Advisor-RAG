import json
import logging
import weaviate
from typing import List,  Union
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter  
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
# from weaviate import EmbeddedOptions
from datasets import Dataset
from dotenv import load_dotenv,find_dotenv
from weaviate.embedded import EmbeddedOptions

 
# Load OpenAI API key from .env file
load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)


def load_file(file_path):
    try:

        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read the contents of the file
            file_contents = file.read()   
        
        return file_contents
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None 

def data_loader(file_path: str, chunk_size: int = 500, chunk_overlap: int = 50) -> Union[List[str], None]:
    """
    Load data from a file, split it into chunks, and return the chunks.

    Parameters:
    - file_path (str): The path to the file containing the data.
    - chunk_size (int): The size of each data chunk. Default is 500.
    - database (int): The overlap between consecutive chunks. Default is 50.

    Returns:
    - list: A list of data chunks.
    """
    try:
        loader = TextLoader(file_path)
        documents = loader.load()

        # Chunk the data
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents(documents)
        
        print("Data loaded to vector database successfully")
        return chunks
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None 
    
    
def create_retriever(chunks):
    try:
        # Load OpenAI API key from .env file
        load_dotenv(find_dotenv())
        #  Setup vector database
        client = weaviate.Client(embedded_options=EmbeddedOptions())

        # Populate vector database using embeddings from the Hugging Face model
        vectorstore = Weaviate.from_documents(
            client=client,
            documents=chunks,
            embedding=OpenAIEmbeddings(),  # Use the model's encode function for embeddings
            by_text=False
        )

        # Define vectorstore as retriever to enable semantic search
        retriever = vectorstore.as_retriever()
        print("Retriever created successfully.")

        return retriever

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def create_langchain_pipeline(retriever, template, temperature=0):
    try:
        # Define LLM
        llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=temperature)

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
    
    

def generate_testcase_and_context(questions, ground_truths, retriever, rag_chain):
    try:
        answers = []
        contexts = []

        # Inference
        for query in questions:

            answers.append(rag_chain.invoke(query))
            contexts.append([docs.page_content for docs in retriever.get_relevant_documents(query)])

            
        data = {
            "question": questions, # list 
            "answer": answers, # list
            "contexts": contexts, # list list
            "ground_truths": ground_truths # list Lists
        }


        # Convert dict to dataset
        dataset = Dataset.from_dict(data) 
        print("automatic evaluation data generated succesfully.")

        return  dataset
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None 


def get_generated_prompt_with_evaulation(question):
    try:
        chunks = data_loader()
        retriever = create_retriever(chunks)

        prompt_template = load_file('../prompts/prompt-generation-prompt.txt')
        evaluation_tempate = load_file('../prompts/evaluation-data-generation.txt')


        prompt_rag_chain = create_langchain_pipeline(retriever, prompt_template)
        evaulation_rag_chain = create_langchain_pipeline(retriever, evaluation_tempate, temperature=0.2)


        generated_prompts = prompt_rag_chain.invoke(question)
        prompt_list  = json.loads(generated_prompts)

        questions = [item['prompt'] for item in prompt_list]
        ground_truths = [[item['ground_truth']] for item in prompt_list]

        response = generate_testcase_and_context(questions, ground_truths, retriever, evaulation_rag_chain)
        return response
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None 
import logging
import weaviate
from typing import List,  Union
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter  
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
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
    

def extract_questions_and_groundtruth(file_path):
    """
    Extracts questions and ground truth answers from a document.

    Args:
        document: A string containing the text document.

    Returns:
        A list of dictionaries, where each dictionary contains:
        - question: The extracted question string.
        - ground_truth_answer: The corresponding ground truth answer string.
    """
    with open(file_path, "r") as file:
        document = file.read()
        
    eval_questions = []
    eval_answers = []
    for line in document.splitlines():
        if line.startswith("Q"):
            eval_questions.append(line[3:])
        elif line.startswith("A"):
            eval_answers.append([line[3:]])

    return eval_questions,eval_answers

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


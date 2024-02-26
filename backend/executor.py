from langchain.agents import  initialize_agent
from langchain.agents import Tool
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.chat_models import ChatCohere
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv
import logging
import os

llm = ChatCohere(temperature=0.1, model='text-davinci-003')
# conversational memory

load_dotenv()
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")

# Create cohere's chat model and embeddings objects
cohere_chat_model = ChatCohere(cohere_api_key=COHERE_API_KEY)
cohere_embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)
raw_documents = TextLoader('./../rag/prompts/context.txt').load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)
db = Chroma.from_documents(documents, cohere_embeddings)
# retrieval qa chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever()
)


conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)


def get_agent_executor(cohere_api_key):
    """
    Initialize and return an executor agent, handling potential errors.

    Args:
        cohere_api_key (str): The Cohere API key.

    Returns:
        The initialized agent executor.

    Raises:
        Exception: If an error occurs during agent executor initialization.
    """

    logging.basicConfig(level=logging.INFO)  # Configure logging for detailed messages

    try:
        # Initialize language model
        llm = ChatCohere(temperature=0.1, model='text-davinci-003', api_key=cohere_api_key)

        # Initialize tools, adding informative descriptions
        tools = [
            Tool(
                name='Knowledge Base',
                func=qa.run,
                description=(
                    "You are an advanced Contract Q&A assistant designed specifically for Lizzy AI's Contract Advisor project. "
                    "Your primary role is to facilitate queries and provide informative responses regarding contract-related inquiries. "
                    "Use the following retrieved context to answer the question. If you don't know the answer, "
                    "acknowledge the lack of information and stop searching after 3 iterations."
                )
            )
        ]

        # Initialize agent executor
        agent_executor = initialize_agent(
            agent='chat-conversational-react-description',
            tools=tools,
            llm=llm,
            verbose=True,
            max_iterations=3,
            early_stopping_method='generate',
            memory=conversational_memory
        )

        return agent_executor

    except Exception as e:
        logging.error(f"Error initializing agent executor: {e}")
        raise Exception("Failed to create agent executor")


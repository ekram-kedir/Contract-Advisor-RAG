from langchain.chat_models import ChatCohere
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import JSONAgentOutputParser


def get_agent_analyst():
    """
    Create and return an analyst agent configured with a predefined prompt and language model.

    Raises:
        Exception: If there is an error reading the system message file.
    """

    try:
        # Read system message from file
        with open("system_message.txt", "r") as file:
            system_message = file.read()

        # Create prompt template for analyst agent
        analyst_prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("user", "{question}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Initialize language model
        llm = ChatCohere(temperature=0.1, model='text-davinci-003')

        # Construct analyst agent pipeline
        analyst_agent = (
            {
                "question": lambda x: x["question"],
                "agent_scratchpad": lambda x: format_to_openai_function_messages(x["intermediate_steps"]),
            }
            | analyst_prompt
            | llm
            | JSONAgentOutputParser()
        )

        return analyst_agent

    except Exception as e:
        raise Exception(f"Error reading system message file: {e}")

from langchain.agents import tool
from pydantic import BaseModel, Field
from typing import List

from rag_utils import get_generated_prompt_with_evaulation, evaluate_prompt
class SQLQuery(BaseModel):
    query: str = Field(description="SQL query to execute")

@tool
def generate_prompts_with_evaluation(query: str) -> List:
    """Returns generated prompts with evaluation"""
    return get_generated_prompt_with_evaulation(query)

@tool
def get_prompt_ranking_monte_carol_and_elo_rating(prompts: list) -> List:
    """Returns generated prompts ranking evaluation using monte carlo and elo rating evaulation"""
    return evaluate_prompt(prompts)



@tool
def generate_evaluation_data(query: str) -> List:
    """Returns geneated evaluation data"""
    return '''
Your task is to formulate exactly the number of questions taken from user {query} or set it to 5 questions from given context and provide the answer to each one.

End each question with a '?' character and then in a newline write the answer to that question using only 
the context provided.
The output MUST BE in a json format. 

example:
[
{
    "user": "What is the name of the company?",
    "assistant": "Google"
},
{
    "user": "What is the name of the CEO?",
    "assistant": "Sundar Pichai"
}
]

Each question must start with "user:".
Each answer must start with "assistant:".


The question must satisfy the rules given below:
1.The question should make sense to humans even when read without the given context.
2.The question should be fully answered from the given context.
3.The question should be framed from a part of context that contains important information. It can also be from tables,code,etc.
4.The answer to the question should not contain any links.
5.The question should be of moderate difficulty.
6.The question must be reasonable and must be understood and responded by humans.
7.Do no use phrases like 'provided context',etc in the question
8.Avoid framing question using word "and" that can be decomposed into more than one question.
9.The question should not contain more than 10 words, make of use of abbreviation wherever possible.
    
context: taken the context from the challenge document provided in the retriver according to user query {query}
'''

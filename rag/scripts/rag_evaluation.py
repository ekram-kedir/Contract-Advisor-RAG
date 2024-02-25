import os
import pandas as pd
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from datasets import Dataset
from dotenv import load_dotenv
from ragas import evaluate
import matplotlib.pyplot as plt
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision,
    context_relevancy,
    answer_correctness,
    answer_similarity,
)

load_dotenv()
openai_api_key=os.environ["OPENAI_API_KEY"]

class RAG:
    def __init__(self):
        self.openai_api_key = openai_api_key
    
    def rag_pipeline(self, template, retriever, model):
        
        prompt = ChatPromptTemplate.from_template(template)

        rag_chain = (
            {"context": retriever, "question": prompt} 
            | model
            | StrOutputParser() 
        )
        return rag_chain

    def create_ragas_dataset(self, questions, answers, rag_pipeline, retriever):
        contexts = []
        for question in questions:
            contexts.append([documents.page_content for documents in retriever.get_relevant_documents(question)])

        data = {
            "question": questions,
            "answer": [rag_pipeline.invoke(question) for question in questions],
            "contexts": contexts,
            "ground_truths": answers
        }
        
        dataset = Dataset.from_dict(data)        
        return dataset

    def evaluate(self, dataset):
        result = evaluate(
        dataset,
        metrics=[
            context_precision,
            faithfulness,
            answer_relevancy,
            context_recall,
            context_relevancy,
            answer_correctness,
            answer_similarity
        ],
    
        )
        return result

    def visualize_evaluation_result(self, rag_evaluate):
        import plotly.graph_objects as go


        data = {
            'context_precision': rag_evaluate['context_precision'],
            'faithfulness': rag_evaluate['faithfulness'],
            'answer_relevancy': rag_evaluate['answer_relevancy'],
            'context_recall': rag_evaluate['context_recall'],
            'context_relevancy': rag_evaluate['context_relevancy'],
            'answer_correctness': rag_evaluate['answer_correctness'],
            'answer_similarity': rag_evaluate['answer_similarity']
        }

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=list(data.values()),
            theta=list(data.keys()),
            fill='toself',
            name='Ensemble RAG'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title='Retrieval Augmented Generation - Evaluation',
            width=800,
        )
        return fig







    



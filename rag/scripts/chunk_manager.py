import re
from typing import List
import matplotlib.pyplot as plt
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    MarkdownTextSplitter
)
from agentic_chunker import AgenticChunker
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain_community.chat_models import ChatOpenAI
from langchain_experimental.text_splitter import SemanticChunker
from langchain.chains import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel
from sklearn.metrics.pairwise import cosine_similarity
from langchain import hub
import os
import numpy as np
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

class ChunkerManager:
    def __init__(self):
        # Load environment variables from the .env file
        dotenv_path = './../../.env'
        load_dotenv(dotenv_path)
        self.openai_api_key = os.environ.get("OPENAI")

    def character_splitting(self, file_path,chunk_size=35, chunk_overlap=0):
        loader = TextLoader(file_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separator='', strip_whitespace=False)
        chunks = text_splitter.split_documents(documents)
        return chunks

    def recursive_character_splitting(self, file_path):
        loader = TextLoader(file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=65, chunk_overlap=0)
        chunks = text_splitter.split_documents(documents)
        return chunks

    def document_specific_splitting(self, file_path):
        loader = TextLoader(file_path)
        documents = loader.load()
        text_splitter = MarkdownTextSplitter(chunk_size=40, chunk_overlap=0)
        chunks = text_splitter.split_documents(documents)
        return chunks

    def semantic_chunking(self, essay):
        # single_sentences_list = re.split(r'(?<=[.?!])\s+', essay)
        # sentences = [{'sentence': x, 'index': i} for i, x in enumerate(single_sentences_list)]
        # sentences = self._combine_sentences(sentences)
        # embeddings = self._embed_sentences(sentences)
        # for i, sentence in enumerate(sentences):
        #     sentence['combined_sentence_embedding'] = embeddings[i]
        # distances, sentences = self._calculate_cosine_distances(sentences)
        # indices_above_thresh = self.plot(distances)
        # chunks = self. _create_semantic_chunks(sentences, indices_above_thresh)
        # return chunks
        text_splitter = SemanticChunker(SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"))
        chunks = text_splitter.create_documents([essay])
        return chunks

    
    def plot(self, distances):
        plt.plot(distances)
        
        y_upper_bound = .2
        plt.ylim(0, y_upper_bound)
        plt.xlim(0, len(distances))

        # We need to get the distance threshold that we'll consider an outlier
        # We'll use numpy .percentile() for this
        breakpoint_percentile_threshold = 95
        breakpoint_distance_threshold = np.percentile(distances, breakpoint_percentile_threshold) # If you want more chunks, lower the percentile cutoff
        plt.axhline(y=breakpoint_distance_threshold, color='r', linestyle='-');

        # Then we'll see how many distances are actually above this one
        num_distances_above_theshold = len([x for x in distances if x > breakpoint_distance_threshold]) # The amount of distances above your threshold
        plt.text(x=(len(distances)*.01), y=y_upper_bound/50, s=f"{num_distances_above_theshold + 1} Chunks");

        # Then we'll get the index of the distances that are above the threshold. This will tell us where we should split our text
        indices_above_thresh = [i for i, x in enumerate(distances) if x > breakpoint_distance_threshold] # The indices of those breakpoints on your list

        # Start of the shading and text
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        for i, breakpoint_index in enumerate(indices_above_thresh):
            start_index = 0 if i == 0 else indices_above_thresh[i - 1]
            end_index = breakpoint_index if i < len(indices_above_thresh) - 1 else len(distances)

            plt.axvspan(start_index, end_index, facecolor=colors[i % len(colors)], alpha=0.25)
            plt.text(x=np.average([start_index, end_index]),
                    y=breakpoint_distance_threshold + (y_upper_bound)/ 20,
                    s=f"Chunk #{i}", horizontalalignment='center',
                    rotation='vertical')

        # # Additional step to shade from the last breakpoint to the end of the dataset
        if indices_above_thresh:
            last_breakpoint = indices_above_thresh[-1]
            if last_breakpoint < len(distances):
                plt.axvspan(last_breakpoint, len(distances), facecolor=colors[len(indices_above_thresh) % len(colors)], alpha=0.25)
                plt.text(x=np.average([last_breakpoint, len(distances)]),
                        y=breakpoint_distance_threshold + (y_upper_bound)/ 20,
                        s=f"Chunk #{i+1}",
                        rotation='vertical')

        plt.title("PG Essay Chunks Based On Embedding Breakpoints")
        plt.xlabel("Index of sentences in essay (Sentence Position)")
        plt.ylabel("Cosine distance between sequential sentences")
        plt.show()

        return indices_above_thresh

    def agentic_chunking(self, essay):
        obj = hub.pull("wfh/proposal-indexing")
        llm = ChatOpenAI(model='gpt-4-1106-preview', openai_api_key=self.openai_api_key)
        runnable = obj | llm
        extraction_chain = self._create_extraction_chain(llm)
        propositions = self._get_propositions(runnable, extraction_chain, essay)
        ac = AgenticChunker()
        ac.add_propositions(propositions)
        chunks = ac.get_chunks(get_type='list_of_strings')
        return chunks

    def _combine_sentences(self, sentences, buffer_size=1):
        for i in range(len(sentences)):
            combined_sentence = ''
            for j in range(i - buffer_size, i):
                if j >= 0:
                    combined_sentence += sentences[j]['sentence'] + ' '
            combined_sentence += sentences[i]['sentence']
            for j in range(i + 1, i + 1 + buffer_size):
                if j < len(sentences):
                    combined_sentence += ' ' + sentences[j]['sentence']
            sentences[i]['combined_sentence'] = combined_sentence
        return sentences

    def _embed_sentences(self, sentences):
        oaiembeds = OpenAIEmbeddings(api_key=self.openai_api_key)
        embeddings = oaiembeds.embed_documents([x['combined_sentence'] for x in sentences])
        return embeddings

    def _calculate_cosine_distances(self, sentences):
        distances = []
        for i in range(len(sentences) - 1):
            embedding_current = sentences[i]['combined_sentence_embedding']
            embedding_next = sentences[i + 1]['combined_sentence_embedding']
            similarity = cosine_similarity([embedding_current], [embedding_next])[0][0]
            distance = 1 - similarity
            distances.append(distance)
            sentences[i]['distance_to_next'] = distance
        return distances, sentences
    
    def _create_semantic_chunks(self,sentences, indices_above_thresh):
        # Initialize the start index
        start_index = 0

        # Create a list to hold the grouped sentences
        chunks = []

        # Iterate through the breakpoints to slice the sentences
        for index in indices_above_thresh:
            # The end index is the current breakpoint
            end_index = index

            # Slice the sentence_dicts from the current start index to the end index
            group = sentences[start_index:end_index + 1]
            combined_text = ' '.join([d['sentence'] for d in group])
            chunks.append(combined_text)
            
            # Update the start index for the next group
            start_index = index + 1

        # The last group, if any sentences remain
        if start_index < len(sentences):
            combined_text = ' '.join([d['sentence'] for d in sentences[start_index:]])
            chunks.append(combined_text)
            
        return chunks

    def _create_extraction_chain(self, llm):
        class Sentences(BaseModel):
            sentences: List[str]

        extraction_chain = create_extraction_chain_pydantic(pydantic_schema=Sentences, llm=llm)
        return extraction_chain

    def _get_propositions(self, runnable, extraction_chain, essay):
        runnable_output = runnable.invoke({"input": essay}).content
        propositions = extraction_chain.run(runnable_output)[0].sentences
        return propositions

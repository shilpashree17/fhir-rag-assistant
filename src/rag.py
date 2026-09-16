'''RAG Steps
1> Document Loading --> Loading the raw data to the system environment
2> Preprocessing -> Ensure Data qualify for the model i.e clean data/remove noise
3> Chunking -> split text into smaller chunks for better processing
4> Embedding -> convert text chunks into vector representation (numbers) as computer understands only numbers
5> Vector Storage -> saves the content to vector DB to enable fast semantic search
6> Retrieval -> Find relavent chuncks based on cosine similarity, fetch data relevant to the user search/query
7> Generating response through LLM- Generate final natural language response
'''
'''chromadb- vector database for storing embeddings
sentence-transformers- model library for generating embeddings from text'''

import os
import chromadb
# from chromadb.utils import embedding_functions
from fhir_client import get_patient_context

'''Set up a path for Chroma Db in project root directory'''

BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CHROMA_DB_PATH=os.path.join(BASE_DIR,"chroma_db")

# Create a persistant client to save data to local directory
client=chromadb.PersistentClient(path=CHROMA_DB_PATH)
# embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection=client.get_or_create_collection("patient_records")#,embedding_function=embedding_fn)

def index_patient(patient_id):
    chunks=get_patient_context(patient_id)
    # print("***chunks***")
    # print(chunks)
    # print("***chunks***")
    if not chunks:
        return 0
    collection.upsert(ids=[f"{patient_id}_{i}" for i in range(len(chunks))],documents=chunks)
    return len(chunks)

def retrieve(query, k=3):
    results=collection.query(query_texts=[query],n_results=k)
    # print(str(results.keys()) + "\n" + str(results.values()))
    return results['documents'][0] if results['documents'] else []

if __name__ == "__main__":
    n= index_patient("2d95f315-808c-4b67-836b-e56bdba9dd21")
    print(f"Indexed {n} chunks for patient ")
    print(retrieve("diabetes"))

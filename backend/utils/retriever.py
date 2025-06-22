# backend/utils/retriever.py
import numpy as np
from .embeddings import get_embedding

def retrieve_relevant_chunks(index, chunks, vectors, query: str, top_k=8):
    query_vector = np.array(get_embedding(query)).astype('float32')
    distances, indices = index.search(np.array([query_vector]), top_k)
    return [chunks[i] for i in indices[0]]

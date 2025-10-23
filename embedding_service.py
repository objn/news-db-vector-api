"""
Google AI Studio (Gemini) Embedding Service
Uses the text-embedding-004 model for generating embeddings
"""

import google.generativeai as genai
from config import settings
from typing import List

# Configure Google AI
genai.configure(api_key=settings.GEMINI_API_KEY)


def generate_embedding(text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> List[float]:
    """
    Generate embedding vector for text using Google's embedding model.
    
    Args:
        text: The text to embed
        task_type: The task type for embedding. Options:
            - "RETRIEVAL_DOCUMENT": For embedding documents in a retrieval system
            - "RETRIEVAL_QUERY": For embedding queries in a retrieval system
            - "SEMANTIC_SIMILARITY": For computing similarity between texts
            - "CLASSIFICATION": For text classification
            - "CLUSTERING": For text clustering
    
    Returns:
        List of float values representing the embedding vector
    """
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type=task_type
        )
        return result['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        raise


def generate_embeddings_batch(texts: List[str], task_type: str = "RETRIEVAL_DOCUMENT") -> List[List[float]]:
    """
    Generate embeddings for multiple texts in batch.
    
    Args:
        texts: List of texts to embed
        task_type: The task type for embedding
    
    Returns:
        List of embedding vectors
    """
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=texts,
            task_type=task_type
        )
        return result['embedding']
    except Exception as e:
        print(f"Error generating batch embeddings: {e}")
        raise


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First embedding vector
        vec2: Second embedding vector
    
    Returns:
        Cosine similarity score between -1 and 1
    """
    import math
    
    # Calculate dot product
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    
    # Calculate magnitudes
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    
    # Calculate cosine similarity
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

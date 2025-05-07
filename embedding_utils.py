import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL
from typing import List

embedding_model = SentenceTransformer(EMBEDDING_MODEL)

def embed_texts(texts: List[str]) -> np.ndarray:
    """Generate embeddings for the given texts."""
    return embedding_model.encode(
        texts,
        convert_to_tensor=False,
        normalize_embeddings=True,
        show_progress_bar=False
    )

def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    """Create an optimized FAISS index from embeddings."""
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(np.array(embeddings).astype('float32'))
    return index
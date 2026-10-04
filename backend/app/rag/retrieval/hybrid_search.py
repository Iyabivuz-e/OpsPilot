
from schemas.document_schema import Document

def hybrid_search(vector_store, all_docs: list[Document], query:str, top_k:int=10):
    # Similarity search
    vector_hits = vector_store.similarity_search
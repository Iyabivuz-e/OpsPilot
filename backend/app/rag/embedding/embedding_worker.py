import asyncio
from .embedding import Embedding, EmbeddingBacher
from core.settings import settings


""" We will put this function in a background task"""

def embedd_document_task(document_id, chunks, model_name=settings.EMBEDDINGS_MODEL):
    embedding = Embedding(model_name)
    batcher = EmbeddingBacher(batch_size=64)
    
    for batch in batcher.get_batches(chunks):
        text_to_embedd = [chunk.content for chunk in batch]
        # print(f"text to embedd {len(text_to_embedd)} for document {document_id}.")
        
        try:
            embeddings = embedding.embed(text_to_embedd)
            print(f"Generated embeddings for document {document_id}.")
            
            payloads = []
            for idx, chunk in enumerate(batch):
                payloads.append({
                    "id": f"{document_id}_{chunk.chunk_index}",
                    "vector": embeddings[idx],
                    "metadata": chunk.metadata
                })
            # Here we save it to thevector store(pgvector) --- later
            return payloads
        except Exception as e:
            # print(f"Failed to generate embeddings for document {document_id}: {e}")
            raise e
    # print(f"the payloads{len(payloads)} for document {document_id}.")

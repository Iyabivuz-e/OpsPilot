import asyncio
from fastapi import Depends
from .embedding import Embedding, EmbeddingBacher
from core.settings import settings
# from sqlalchemy.orm import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Document
from database.db import get_db

""" We will put this function in a background task"""

async def embedd_document_task(
    document_id, 
    chunks, 
    db: AsyncSession, 
    model_name=settings.EMBEDDINGS_MODEL):
    
    embedding = Embedding(model_name)
    batcher = EmbeddingBacher(batch_size=64)
    
    for batch in batcher.get_batches(chunks):
        text_to_embedd = [chunk.content for chunk in batch]
        # print(f"text to embedd {len(text_to_embedd)} for document {document_id}.")
        
        try:
            embeddings = embedding.embed(text_to_embedd)
            print(f"Generated embeddings for document {document_id}.")
            print("embeddings type:", type(embeddings))
            print("embeddings[0] type:", type(embeddings[0]))
            print("embeddings[0] repr:", repr(embeddings[0])[:500])

            
            payloads = []
            for idx, chunk in enumerate(batch):
                payloads.append({
                    "id": f"{document_id}_{chunk.chunk_index}",
                    "vector": embeddings[idx],
                    "metadata": chunk.metadata
                })
            print(type(embeddings[idx]))
            print(embeddings[idx][:5])
            # Here we save it to thevector store(pgvector) --- later
            payload_sqlalchemy = []
            for pl in payloads:
                # We convert the payload dict into a SQLAlchemy Document
                db_obj = Document(
                    id=pl["id"],
                    embeddings=pl["vector"],
                    doc_metadata=pl["metadata"]
                )

                payload_sqlalchemy.append(db_obj)
            db.add_all(payload_sqlalchemy)
            await db.commit()
            # return payloads
        
        except Exception as e:
            # print(f"Failed to generate embeddings for document {document_id}: {e}")
            raise e
    # print(f"the payloads{len(payloads)} for document {document_id}.")

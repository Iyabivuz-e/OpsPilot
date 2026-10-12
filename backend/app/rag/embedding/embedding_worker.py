from .embedding import Embedding, EmbeddingBacher
from core.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Chunk
from uuid import UUID

""" We will put this function in a background task"""

async def embedd_document_task(
    document_version_id, 
    chunks, 
    db: AsyncSession, 
    model_name=settings.EMBEDDINGS_MODEL):
    
    embedding = Embedding(model_name)
    batcher = EmbeddingBacher(batch_size=64)
    
    for batch in batcher.get_batches(chunks):
        text_to_embedd = [chunk.content for chunk in batch]
        
        try:
            embeddings = embedding.embed(text_to_embedd)
            
            payloads = []
            for idx, chunk in enumerate(batch):
                payloads.append({
                    "id": chunk.id,
                    "document_version_id": chunk.document_version_id,
                    "chunk_index": chunk.chunk_index,
                    "content": chunk.content,
                    "content_hash": chunk.content_hash,
                    "embedding": embeddings[idx],
                    "chunk_metadata": chunk.chunk_metadata
                })
            print(type(embeddings[idx]))
            print(embeddings[idx][:5])
            payload_sqlalchemy = []
            for pl in payloads:
                # We convert the payload dict into a SQLAlchemy Document
                db_obj = Chunk(
                    id=UUID(pl["id"]),
                    document_version_id=pl["document_version_id"],
                    chunk_index=pl["chunk_index"],
                    content=pl["content"],
                    content_hash=pl["content_hash"],
                    embedding=pl["embedding"],
                    chunk_metadata=pl["chunk_metadata"]
                )
                

                payload_sqlalchemy.append(db_obj)
            db.add_all(payload_sqlalchemy)
            await db.flush()
            
            return payload_sqlalchemy
        
        except Exception as e:
            raise e

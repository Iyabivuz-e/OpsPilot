from sqlalchemy import select, func
from fastapi import Depends
from database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.document_schema import Document
from models.models import Chunk, DocumentModel, DocumentVersion, DocumentStatus


# We first filter the version of the doucment to be retrieved. only current verion and ready only
def allowed_chunks():
    return (
        select(
            Chunk.id,
            Chunk.content,
            Chunk.chunk_metadata,
            DocumentModel.title,
        )
        .join(
            DocumentVersion,
            DocumentVersion.id == Chunk.document_version_id,
        )
        .join(
            DocumentModel,
            DocumentModel.id == DocumentVersion.document_id,
        )
        .where(
            DocumentModel.current_version_id == DocumentVersion.id,
            DocumentVersion.status == DocumentStatus.ACTIVE.value,
        )
    )
    

async def hybrid_search(
    query: str,
    embedding_fn,
    top_k: int = 5,
    candidates: int = 20,
    rrf_k: int = 60,
    db: AsyncSession = Depends(get_db),
    ):
    
    base = allowed_chunks()
    
    ## Similarity search with embeddings
    vector_hits = (
            base.order_by(
            Chunk.embedding.cosine_distance(embedding_fn(query)).asc()
        ).limit(candidates)
    )
    
    ## Keyword search with tsvector
    tsquery = func.websearch_to_tsquery('english', query)
    keyword_hits = (
            base.order_by(
                Chunk.tsv.op('@@')(tsquery)
        ).order_by(
            func.ts_rank_cd(Chunk.tsv, tsquery).desc()
        ).limit(candidates)
    )
    
    vector_docs = await db.execute(vector_hits)
    keyword_docs = await db.execute(keyword_hits)
    
    ## Reciprocal Rank Fusion (RRF) to combine the results from both searches
    scores, rows = {}, {}
    for results in (vector_docs, keyword_docs):
        for rank, row in enumerate(results):
            row_id = row._mapping["id"]
            scores[row_id] = scores.get(row_id, 0) + 1 / (rrf_k + rank + 1)
            rows[row_id] = row._mapping
            
    best_ids = sorted(scores, key=scores.get, reverse=True)[:top_k]
    
    top_k_docs = [dict(rows[i], scores=scores[i]) for i in best_ids]
    print("Top K docs: ", top_k_docs)
    return top_k_docs
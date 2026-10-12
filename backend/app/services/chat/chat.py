from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from rag.embedding.embedding import Embedding
from core.settings import settings
from rag.retrieval.hybrid_search import hybrid_search

async def completion(
    query: str,
    db: AsyncSession = Depends(get_db),
    embedding_model = Embedding(settings.EMBEDDINGS_MODEL)
,
):
    """
    Handle chat requests by performing a hybrid search and generating a response.
    ------ Will come back to this ---------
    """

    search = await hybrid_search(query, embedding_fn=embedding_model.embed, db=db)

    return search



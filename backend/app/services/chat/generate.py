from rag.retrieval.hybrid_search import hybrid_search
from rag.embedding.embedding import Embedding
from core.settings import settings
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from rag.prompts.construct_prompt import construct_prompt
from core.settings import settings
from groq import Groq
import asyncio

async def generate_answers(
    query: str,
    conversation_history: list[dict],
    db: AsyncSession = Depends(get_db),
):
    embedding_model = Embedding(settings.EMBEDDINGS_MODEL)
    # 1. Retrieve relevant documents
    retrieve = await hybrid_search(query, embedding_fn=embedding_model, db=db)
    # 2. Construct the prompt
    prompt = construct_prompt(retrieve, conversation_history)
    # 3. Call the LLM
    
    client = Groq(api_key=settings.LLM_API_KEY,)
    
    try:
        completions = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model = settings.LLM_MODEL,
            temperature=0.7,
            max_completion_tokens=2048,
            stream=True,
        ) 
        
        for chunk in completions:
            if chunk.choices and chunk.choices[0].delta.content:
                
                token = yield chunk.choices[0].delta.content
                
                # This will help for SSE streaming
                yield f"data: {token}\n\n"
                
                await asyncio.sleep(0) 
                
        yield "data: [DONE]\n\n"
      
    # If anything happens mid stream -- later we shall return gracefully to the client  
    except asyncio.CancelledError as e:
        raise e
    
    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"
import os
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.document_schema import Section
from helpers.mime_types import extension_to_mime
from .extractors.normalizer import normalize_document
from .extractors.registry import registry
from helpers.build_section import build_sections
from .chunking.chunk import chunk_sections 
from .embedding.embedding_worker import embedd_document_task
from .retrieval.hybrid_search import hybrid_search

async def pipeline(file_path: str, db: AsyncSession) -> list[Section]:
    extension = os.path.splitext(file_path)[1].lower()
    mime_type = extension_to_mime.get(extension)
    if not mime_type:
        raise ValueError(f"Unsupported file extension: {extension}")
    
    extractor = registry.get_extractor(mime_type)
    document = extractor.extract(file_path)
    document = normalize_document(document)
    sections = build_sections(document.elements)
    chunks = chunk_sections(document.id, sections)
    embeddings = await embedd_document_task(document.id, chunks, db=db)
    search = await hybrid_search("example query", embedding_fn=embeddings, db=db)
    # return embeddings
    
    ## Run the pipeline with a sample file path
    # file_path = "/Users/dieudonne/Developer/BIP/OpsPilot/OpsPilot/cortora_docs/employee-handbook.pdf"  # Replace with your file path
    # try:
    #     search_results = pipeline(file_path)
    #     print(f"Search Results: {search_results}")
    # except Exception as e:
    #     print(f"Error processing document: {e}")
        
        
    return search
    
from schemas.document_schema import Chunk, Section, Element, ElementType
from core.settings import settings
import hashlib

def build_chunk(document_id_version: str, chunk_index: int, section: Section, text: str) -> Chunk:
    ## We check for the content of the section and get the chunks
    # header = build_header(section)
    # body = "\n\n".join(get_text(element) for element in elements)
    # content = f"{header}\n\n{body}" 
    
    content = f"{section.title}\n\n{text}" if section.title else text ## I have an issue here with the text

    return Chunk(
       document_id_version=document_id_version,
       chunk_index=chunk_index,
       content=content,
       content_hash=hash_content(content),
       tokens=count_tokens(content),
       metadata={
           "section_id": section.id,
           "section_title": section.title,
           #"section_path": section.path,
        #    "element_ids": element_ids,
        #    "pages": pages,
        #     "element_types": types,
            # "chunk_token_count": count_tokens(content)
            
       }
    )
    
## We split the text into pieces of max_tokens, breaking on the nicest boundary available
def split_text(text: str, max_tokens: int, overlap_tokens: int = 0) -> list[str]:
    """Split long text into pieces near max_tokens, breaking on the
    nicest boundary available (blank line, then line, then sentence)."""
    max_chars = max_tokens * 4
    overlap_chars = overlap_tokens * 4
    pieces = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + max_chars, n)
        if end < n:
            for sep in ("\n\n", "\n", ". "):
                boundary = text.rfind(sep, start, end)
                if boundary > start:
                    end = boundary + len(sep)
                    break
        piece = text[start:end].strip()
        if piece:
            pieces.append(piece)
        start = max(end - overlap_chars, start + 1)

    return pieces

def hash_content(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()

def count_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, len(text) // 4)  


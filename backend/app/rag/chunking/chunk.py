
from schemas.document_schema import Chunk, Section, Element, ElementType
from core.settings import settings
from .utils import build_chunk, count_tokens, split_text

def chunk_sections(document_id_version: str, sections: list[Section]) -> list[Chunk]: 

    chunks = []
    for section in sections:
        # assert isinstance(section, Section), f"Expected Section, got {type(section)}"
        chunks.extend(chunk_section(document_id_version, section, len(chunks)))
    return chunks

def chunk_section(document_id_version: str, section: Section, chunk_index: int = 0) -> list[Chunk]:
    chunks = []
    current_elements: list[Element] = [] ## List to hold elements for the current chunk to respct the max token limit
    current_tokens = 0
    index = chunk_index
    
    # This function will help to flush/clean the current_elements list and reset the token count when we reach the max token limit
    def flush():
        nonlocal current_elements, current_tokens, index
        
        if not current_elements:
            return
        chunks.append(build_chunk(document_id_version, index, section, "\n\n".join(current_elements)))
        index += 1
        current_elements = []
        current_tokens = 0
        
    for element in section.elements:
        element_tokens = count_tokens(element.text)
        
        if element_tokens > settings.MAX_TOKENS:
            flush()
            for piece in split_text(element.text, settings.MAX_TOKENS, settings.OVERLAP_TOKENS):
                chunks.append(build_chunk(document_id_version, index, section, piece))
                index += 1
            continue
        
        if element_tokens + current_tokens > settings.MAX_TOKENS:
            flush()
        
        current_elements.append(element.text)
        current_tokens += element_tokens
        
    flush()
    return chunks
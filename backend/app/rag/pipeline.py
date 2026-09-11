import os
from schemas.document_schema import Section
from helpers.mime_types import extension_to_mime
from .extractors.normalizer import normalize_document
from .extractors.registry import registry
from helpers.build_section import build_sections

def pipeline(file_path: str) -> list[Section]:
    extension = os.path.splitext(file_path)[1].lower()
    mime_type = extension_to_mime.get(extension)
    if not mime_type:
        raise ValueError(f"Unsupported file extension: {extension}")
    
    extractor = registry.get_extractor(mime_type)
    document = extractor.extract(file_path)
    document = normalize_document(document)
    sections = build_sections(document.elements)
    # chunks = 
    # embeddings = 
    return sections
    # return embeddings
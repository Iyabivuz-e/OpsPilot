import os
from schemas.document_schema import Document
from helpers.mime_types import extension_to_mime
from .normalizer import normalize_document
from .registry import registry

def pipeline(file_path: str) -> Document:
    extension = os.path.splitext(file_path)[1].lower()
    mime_type = extension_to_mime.get(extension)
    if not mime_type:
        raise ValueError(f"Unsupported file extension: {extension}")
    
    extractor = registry.get_extractor(mime_type)
    document = extractor.extract(file_path)
    document = normalize_document(document)
    print(f"Extracted and normalized document: {document}")
    return document
""" Here we define all classes for extracting text from different file types."""

from abc import ABC, abstractmethod
from schemas.document_schema import Document, Element, ElementType, Section

class BaseExtractor(ABC):
    ## check whether the extractor supports the given file type
    @abstractmethod
    def supports(self, mime_type: str) -> bool: ...
    
    ## extract text from the given file and return a Document object
    @abstractmethod
    def extract(self, file_path: str) -> Document: ...
    
## We do a pdf extractor and the rest will be implemented in the future
class PDFExtractor(BaseExtractor):
    def supports(self, mime_type: str) -> bool:
        return mime_type == "application/pdf"
    
    def extract(self, file_path: str) -> Document:
        import pymupdf
        doc = pymupdf.open(file_path)
        ## for debugging
        # print(f"my document has {doc.page_count} pages: and is {doc.name}")
        elements: list[Element] = []
        ## We then extract the text from each page
        for page_number, page in enumerate(doc, start=1):
             ## Detect tables
            tables = _detect_tables(page)
            for block in page.get_text("dict")["blocks"]:
                if block.get("type") != 0: # if the block is not a text block
                    continue
                text = " ".join(
                    span["text"] for line in block["lines"] for span in line["spans"] 
                ).strip()
                font_size = block["lines"][0]["spans"][0]["size"] if block["lines"] else 10
                font = block["lines"][0]["spans"][0]["font"] if block["lines"] else "default"
                is_bold = any(
                    span["flags"] & 2**4
                    for line in block["lines"]
                    for span in line["spans"]
                )
                print(f"text={text[:40]!r} font={font!r} size={font_size} is_bold={is_bold}")

                element_type = (
                    ElementType.HEADING
                    if font_size >= 14 and is_bold and len(text.split()) < 12
                    else ElementType.PARAGRAPH
                )
                elements.append(Element(
                    type=element_type,
                    text=text,
                    page=page_number
                ))
            for table in tables:
                elements.append(Element(
                    type=ElementType.TABLE,
                    text=table,
                    page=page_number
                ))
                
        meta = doc.metadata or {}
        document =  Document(
            source_uri=file_path,
            mime_type="application/pdf",
            metadata={"title": meta.get("title"), 
                      "author": meta.get("author"), 
                      "subject": meta.get("subject"), 
                      "keywords": meta.get("keywords")},
            elements=elements
        )
            # print(f"Extracted {len(elements)} texts from {document.source_uri}.")
        return document
    
def _detect_tables(page):
    tables = page.find_tables()
    return [table.to_markdown() for table in tables]


## We can add more:: maybe a WordExtractor, HTMLExtractor, etc. in the future
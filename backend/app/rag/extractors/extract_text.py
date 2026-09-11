""" Here we define all classes for extracting text from different file types."""

from abc import ABC, abstractmethod
from schemas.document_schema import Document, Element, ElementType

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
            for block in page.get_text("dict")["blocks"]:
                if block.get("type") != 0: # if the block is not a text block
                    continue
                text = " ".join(
                    span["text"] for line in block["lines"] for span in line["spans"] 
                ).strip()
                # We get the font size of the first span in the block, otherwise we use 10 as a default
                font_size = block["lines"][0]["spans"][0]["size"] if block["lines"] else 10 
                font = block["lines"][0]["spans"][0]["font"] if block["lines"] else "default"
                
                # we then get the element type
                # this is a heuristic based on the font size, boldness, sarrounding text, 
                element_type = (
                    ElementType.HEADING 
                    if font_size > 14 and "bold" in font.lower()
                    and len(text.split()) < 12 
                    else ElementType.PARAGRAPH
                    )
                
                elements.append(Element(
                    type=element_type,
                    text=text,
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
    
## We can add more:: maybe a WordExtractor, HTMLExtractor, etc. in the future
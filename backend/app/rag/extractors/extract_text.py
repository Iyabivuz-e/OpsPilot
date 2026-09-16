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
        elements: list[Element] = []
        
        ## We then extract the text from each page
        for page_number, page in enumerate(doc, start=1):
            for block in page.get_text("dict")["blocks"]:
                if block.get("type") != 0: # if the block is not a text block
                    continue
                
                
                 ## Detect tables
                tables = _detect_tables(page)
                table_bboxes = [table.bbox for table in tables]
                text_bbox = list(block["bbox"])
                
                if any(_bbox_inside(text_bbox, table_bbox) for table_bbox in table_bboxes):
                    continue  # Skip text blocks that are inside tables
                
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
                    page=page_number,
                    bbox = text_bbox
                ))
            for table in tables:                
                elements.append(Element(
                    type=ElementType.TABLE,
                    text=table.to_markdown(),
                    page=page_number,
                    bbox = list(table.bbox)
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
    return tables

## we check whether the text block is in the table boundaries
def _bbox_inside(inner, outer):
    ix0, iy0, ix1, iy1 = inner
    ox0, oy0, ox1, oy1 = outer

    return (
        ix0 >= ox0
        and iy0 >= oy0
        and ix1 <= ox1
        and iy1 <= oy1
    )
## We can add more:: maybe a WordExtractor, HTMLExtractor, etc. in the future
"""This is a helper module to build sections from the extracted text from the PDFs(document)
So that we can have a structure aware chunking.
"""

from schemas.document_schema import Document,Element, ElementType, Section

def build_sections(elements: list[Element]) -> list[Section]:
    sections: list[Section] = []
    current_section: Section | None = None
    
    for element in elements:
        if element.type == ElementType.HEADING:
            current_section = Section(
                title=element.text,
                elements=[]
            )
            sections.append(current_section)
        elif current_section is not None:
            current_section.elements.append(element)

    return sections
"""We normalize the extracted text"""

import re
from collections import Counter
import unicodedata
from schemas.document_schema import Element, Document


def normalize_document(document: Document) -> Document:
    document.elements = [_normalize_text(element) for element in document.elements]
    # document.elements = [_remove_duplicated_lines(element) for element in document.elements]
    document.elements = _remove_duplicated_lines(document.elements)
    return document

## We clean the text by normalizing unicode characters, removing hyphenation, and splitting into words.
def _normalize_text(element: Element) -> Element:
    text = unicodedata.normalize("NFKC", element.text)
    text = re.sub(r"-\n(\w)", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    element.text = text
    return element

## We check if there could be any duplicates
def _remove_duplicated_lines(elements: list[Element]) -> list[Element]:
    counts = Counter(element.text for element in elements if element.text)
    n_pages = len({element.page for element in elements if element.page }) or 1
    noisy = {t for t, c in counts.items() if n_pages > 3 and c / n_pages > 0.5}
    return [e for e in elements if e.text not in noisy]

    



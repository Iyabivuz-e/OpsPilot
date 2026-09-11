"""In this class, we register all the extractors that are available."""

from .extract_text import BaseExtractor, PDFExtractor


class ExtractorRegistry:
    def __init__(self):
        self._extractors: list[BaseExtractor] = []

    def register(self, extractor: BaseExtractor):
        self._extractors.append(extractor)

    def get_extractor(self, mime_type: str):
        for extractor in self._extractors:
            if extractor.supports(mime_type):
                return extractor
        raise ValueError(f"No extractor found for MIME type: {mime_type}")
    
    
registry = ExtractorRegistry()

registry.register(PDFExtractor())
## We can add more extractors here in the future, for example:
# registry.register(DocxExtractor())
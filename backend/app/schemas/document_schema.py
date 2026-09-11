from pydantic import BaseModel, Field
from enum import Enum
from typing import Any
import uuid


class ElementType(str, Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST_ITEM = "list_item"
    TABLE = "table"

class Element(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: ElementType = ElementType.PARAGRAPH
    text: str = ""
    page: int | None = None
    
class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_uri: str
    mime_type: str
    metadata : dict[str, Any] 
    elements: list[Element]
    
    
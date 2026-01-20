from pydantic import BaseModel
from typing import List, Optional


class IMDFManifest(BaseModel):
    version: str
    created: str
    language: str
    generated_by: Optional[str] = None
    extensions: Optional[List[str]] = None

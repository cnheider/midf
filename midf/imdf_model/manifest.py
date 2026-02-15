from typing import List, Optional

from pydantic import BaseModel


class IMDFManifest(BaseModel):
    version: str
    created: str
    language: str
    generated_by: Optional[str] = None
    extensions: Optional[List[str]] = None

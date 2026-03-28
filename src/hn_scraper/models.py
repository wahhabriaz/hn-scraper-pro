from datetime import datetime
from pydantic import BaseModel, HttpUrl, field_validator


class Story(BaseModel):
    id: int
    rank: int
    title: str
    url: str | None = None
    domain: str | None = None
    points: int = 0
    author: str
    comments: int = 0
    scraped_at: datetime

    @field_validator("title")
    @classmethod
    def strip_title(cls, v: str) -> str:
        return v.strip()

    def fingerprint(self) -> str:
        """Used for deduplication."""
        import hashlib
        key = f"{self.id}-{self.title}-{self.author}"
        return hashlib.sha256(key.encode()).hexdigest()
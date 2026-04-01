from pydantic import BaseModel


class Headline(BaseModel):
    text: str
    variant: int


class CopywriterOutput(BaseModel):
    headlines: list[Headline]
    body: str
    cta: str

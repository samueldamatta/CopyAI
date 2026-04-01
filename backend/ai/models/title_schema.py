from pydantic import BaseModel


class TitleOutput(BaseModel):
    title: str

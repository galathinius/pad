from pydantic import BaseModel


class Text(BaseModel):
    text: str


class Chunk(BaseModel):
    chunk: str
    text_id: str
    chunk_idx: int


class TextId(BaseModel):
    text_id: str

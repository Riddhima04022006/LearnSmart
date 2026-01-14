from typing import List
from pydantic import BaseModel
class TopicItem(BaseModel):
    topic: str
    outline: List[str]
class TopicGroups(BaseModel):
    five_plus: List[TopicItem] = []
    three_four: List[TopicItem] = []
class TopicResponse(BaseModel):
    groups: dict

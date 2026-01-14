import re
from typing import List
IGNORE_PATTERN=re.compile(r"^\s*(unit|chapter|part)\s*[-:]?\s*\d+",re.IGNORECASE)
def parse_syllabus_topics(syllabus_text:str)->List[str]:
    topics=[]
    for line in syllabus_text.splitlines():
        clean=line.strip()
        if not clean:continue
        if IGNORE_PATTERN.match(clean):continue
        topics.append(clean)
    return topics

import re
from rapidfuzz import fuzz
from typing import Dict,List
from core.config import FUZZY_MATCH_THRESHOLD,GROUP_5_PLUS,GROUP_3_4_MIN,GROUP_3_4_MAX,GROUP_2_TIMES
def normalize_text(text:str)->str:
    text=text.lower()
    text=re.sub(r"[^a-z0-9\s]"," ",text)
    text=re.sub(r"\s+"," ",text)
    return text.strip()
def extract_topics_from_syllabus(syllabus_text:str)->List[str]:
    topics=[]
    for line in syllabus_text.splitlines():
        line=line.strip()
        if not line:continue
        line=re.sub(r"[–—]","-",line)
        if re.search(r"\b(unit|chapter|part)\b",line,re.IGNORECASE):continue
        parts=re.split(r",|&|:",line)
        for part in parts:
            part=part.strip().lower()
            part=re.sub(r"[^a-z\s]","",part)
            words=part.split()
            if len(words)<2:continue
            if len(part)<8:continue
            topics.append(part)
    return list(set(topics))
def count_topic_occurrences(topic:str,ocr_text:str)->int:
    topic_words=topic.split()
    ocr_tokens=ocr_text.split()
    count=0
    for word in topic_words:
        for token in ocr_tokens:
            if fuzz.partial_ratio(word,token)>=FUZZY_MATCH_THRESHOLD:
                count+=1
                break
    return count
def detect_topics(ocr_text:str,syllabus_text:str)->Dict[str,Dict]:
    ocr_text=normalize_text(ocr_text)
    topics=extract_topics_from_syllabus(syllabus_text)
    topic_counts={}
    for topic in topics:
        freq=count_topic_occurrences(topic,ocr_text)
        if freq>0:topic_counts[topic]=freq
    groups={"5_plus":[],"3_4":[],"2_times":[]}
    for topic,freq in topic_counts.items():
        if freq>=GROUP_5_PLUS:
            groups["5_plus"].append({"topic":topic.title(),"outline":["Definition","Key concepts","Examples","Advantages","Applications"]})
        elif GROUP_3_4_MIN<=freq<=GROUP_3_4_MAX:
            groups["3_4"].append({"topic":topic.title(),"outline":["Definition","Explanation","Example"]})
        elif freq==GROUP_2_TIMES:
            groups["2_times"].append({"topic":topic.title(),"outline":["Definition","Explanation","Example"]})
    return {"groups":groups}

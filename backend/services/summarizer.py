import spacy,numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
nlp=spacy.load("en_core_web_sm")
def summarize_text(text:str,max_words:int=350)->str:
    if not text:return ""
    doc=nlp(text)
    sentences=[sent.text.strip() for sent in doc.sents]
    if not sentences:return ""
    vectorizer=TfidfVectorizer(stop_words="english")
    x=vectorizer.fit_transform(sentences)
    scores=np.asarray(x.sum(axis=1)).ravel()
    ranked_indices=scores.argsort()[::-1]
    summary_sentences=[]
    current_word_count=0
    for idx in ranked_indices:
        sentence=sentences[idx]
        sentence_word_count=len(sentence.split())
        if current_word_count+sentence_word_count>max_words:continue
        summary_sentences.append((idx,sentence))
        current_word_count+=sentence_word_count
        if current_word_count>=max_words:break
    summary_sentences.sort(key=lambda x:x[0])
    return " ".join(sentence for _,sentence in summary_sentences)

import wikipedia,re
def _strip_wiki_sections(text:str)->str:
    STOP_SECTIONS=["== References ==","== Further reading ==","== External links ==","== See also =="]
    for section in STOP_SECTIONS:
        idx=text.find(section)
        if idx!=-1:text=text[:idx]
    return text
def _strip_math_artifacts(text:str)->str:
    text=re.sub(r"\{\\displaystyle.*?\}","",text)
    text=re.sub(r"\bO\s*\(\s*n\s*\d+\s*\)","O(n)",text)
    return text
def _strip_nav_lines(text:str)->str:
    lines=text.splitlines();clean_lines=[]
    for line in lines:
        line=line.strip()
        if not line:continue
        if len(line.split())<5:continue
        clean_lines.append(line)
    return "\n".join(clean_lines)
def get_wikipedia_text(topic:str)->str:
    try:
        page=wikipedia.page(topic,auto_suggest=True);text=page.content
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            page=wikipedia.page(e.options[0],auto_suggest=True);text=page.content
        except Exception:return ""
    except wikipedia.exceptions.PageError:
        results=wikipedia.search(topic)
        if not results:return ""
        try:
            page=wikipedia.page(results[0],auto_suggest=True);text=page.content
        except Exception:return ""
    except Exception:return ""
    text=_strip_wiki_sections(text)
    text=_strip_math_artifacts(text)
    text=_strip_nav_lines(text)
    return text

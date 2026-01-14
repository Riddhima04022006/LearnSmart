from fastapi import FastAPI,UploadFile,File,Form,BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uuid,os
from core.ocr import extract_text_from_images
from storage.temp import create_job_dir,write_ocr_output,TEMP_ROOT,delete_job_dir
from services.topic_detector import detect_topics
from services.summarizer import summarize_text
from services.wikipedia_service import get_wikipedia_text
from pydantic import BaseModel
app=FastAPI(title="LearnSmart API")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
class TopicRequest(BaseModel):topic:str
class SummaryResponse(BaseModel):summary:str
@app.get("/")
def root():return{"status":"ok","message":"LearnSmart backend running"}
@app.post("/upload")
async def upload_files(files:List[UploadFile]=File(...),syllabusText:str=Form("")):
    job_id=str(uuid.uuid4());job_dir=create_job_dir(job_id)
    ocr_texts=await extract_text_from_images(files,job_dir);write_ocr_output(job_dir,ocr_texts)
    with open(os.path.join(job_dir,"syllabus.txt"),"w",encoding="utf-8") as f:f.write(syllabusText)
    return{"job_id":job_id,"pages_processed":len(ocr_texts),"status":"OCR completed, analysis pending"}
@app.get("/api/topic/{job_id}")
def get_results(job_id:str,background_tasks:BackgroundTasks):
    job_dir=os.path.join(TEMP_ROOT,job_id);ocr_path=os.path.join(job_dir,"ocr_output.txt");syllabus_path=os.path.join(job_dir,"syllabus.txt")
    if not os.path.exists(ocr_path) or not os.path.exists(syllabus_path):return{"groups":{"5_plus":[],"3_4":[]}}
    with open(ocr_path,"r",encoding="utf-8") as f:ocr_text=f.read()
    with open(syllabus_path,"r",encoding="utf-8") as f:syllabus_text=f.read()
    background_tasks.add_task(delete_job_dir,job_id);return detect_topics(ocr_text,syllabus_text)
@app.post("/api/summarize",response_model=SummaryResponse)
def summarize_topic(request:TopicRequest):
    wiki_text=get_wikipedia_text(request.topic);summary=summarize_text(wiki_text)
    return{"summary":summary}

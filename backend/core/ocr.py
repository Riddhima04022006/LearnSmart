import os,shutil
from typing import List
from fastapi import UploadFile
import easyocr
ocr_reader=easyocr.Reader(['en'],gpu=False)
async def extract_text_from_images(files:List[UploadFile],job_dir:str)->List[str]:
    extracted_texts=[]
    for file in files:
        file_path=os.path.join(job_dir,file.filename)
        with open(file_path,"wb") as buffer:shutil.copyfileobj(file.file,buffer)
        try:
            result=ocr_reader.readtext(file_path,detail=0)
            extracted_texts.append("\n".join(result))
        except Exception:
            extracted_texts.append("")
        os.remove(file_path)
    return extracted_texts

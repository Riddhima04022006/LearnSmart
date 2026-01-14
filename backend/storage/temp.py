import os
import shutil
TEMP_ROOT = "temp_uploads"
os.makedirs(TEMP_ROOT, exist_ok=True)
def create_job_dir(job_id: str) -> str:
    path = os.path.join(TEMP_ROOT, job_id)
    os.makedirs(path, exist_ok=True)
    return path
def write_ocr_output(job_dir: str, texts: list):
    path = os.path.join(job_dir, "ocr_output.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(texts))
def delete_job_dir(job_id: str):
    path = os.path.join(TEMP_ROOT, job_id)
    if os.path.exists(path):
        shutil.rmtree(path)
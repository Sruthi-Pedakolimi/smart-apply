from fastapi import FastAPI
from fastapi import UploadFile
from pypdf import PdfReader

app = FastAPI()


@app.post('/upload')
async def upload_file(file: UploadFile):
    """
        It accepts the single pdf file and returns the content
    """
    text = ""
    # read the file content
    content = PdfReader(file.file)
    for page in content.pages:
        text += page.extract_text()
    
    return text

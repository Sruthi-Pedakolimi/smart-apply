import os 
import json
from fastapi import FastAPI
from fastapi import UploadFile
from pypdf import PdfReader
from dotenv import load_dotenv
from openai import OpenAI

# system prompt
SYSTEM_PROMPT = """You are a career expert where you take the uploaded resume file text and job description mentioned and return a structured JSON format 
                 {"ats_score": ATS score, "cover_letter": Cover Letter} 
                 
                 Please follow below guidelines while working on cover letter
                 1. It should be of international standards.
                 2. It shouldn't be generic. Personalize it based on the resume and job description and company
                 3. No dashes, double dashes or colons ("--", "-", ";", ":")
                 4. Use simple natural english
                 
                 IMPORTANT: You should only return the JSON structure mentioned, nothing else.
                 """

# loading the env
load_dotenv(override=True)
api_key = os.getenv("OPEN_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

# create instances of FastAPI and OpenAI
app = FastAPI()
client = OpenAI(api_key=api_key, base_url=base_url)

# get data will take the inputs of the file and job description and returns the dict contains ats_score and cover_letter
@app.post('/info')
async def get_data(file: UploadFile, job: str):
    """
        It accepts the single pdf file and returns the content
    """
    text = ""
    # read the file content
    content = PdfReader(file.file)
    for page in content.pages:
        text += page.extract_text()
    
    # sending the input to the open AI
    conversation = client.conversations.create()
    response = client.responses.create(
         model="gpt-4.1",
          input=[{"role": "system", "content": SYSTEM_PROMPT},
                 {"role": "user", "content": f"Resume: {text}\n\nJob Description: {job}" }],
          conversation = conversation.id,
    )
    output_text = response.output[0].content[0].text
    # convert the json string to dict
    output_json = json.loads(output_text)
    return output_json
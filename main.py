import os 
import json
from fastapi import FastAPI
from fastapi import UploadFile, Form
from pypdf import PdfReader
from dotenv import load_dotenv
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware


# system prompt
SYSTEM_PROMPT = """You are a career expert where you take the uploaded resume file text and job description mentioned and return a structured JSON format 
                 {"ats_score": ATS score, "cover_letter": Cover Letter} 
                 
                 Please follow below guidelines while working on cover letter
                 1. It should be of international standards.
                 2. It shouldn't be generic. Personalize it based on the resume and job description and company
                 3. No dashes, double dashes or colons ("--", "-", ";", ":")
                 4. Use simple natural english
                 5. Strict Use of resume experience that is related and don't create something new which is not in my resume. 
                 Understand my experience projects etc and then u can create from that but not totally new experience
                 6. While calculating the ATS score make sure you check whether the JD matches the Resume uploaded based on below criteria
                 *** score based on: keywords 30%, skills 30%, experience 25%, education 15%
                 IMPORTANT: You should only return the JSON structure mentioned, nothing else.
                 """

# loading the env
load_dotenv(override=True)
api_key = os.getenv("OPEN_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

# create instances of FastAPI and OpenAI
app = FastAPI()
client = OpenAI(api_key=api_key, base_url=base_url)

# origins for CORS
origins = [
    "http://localhost:5173",
     "http://localhost",
]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["GET", "POST", "PUT"], allow_headers=["Authorization", "Content-Type"])
# get data will take the inputs of the file and job description and returns the dict contains ats_score and cover_letter
@app.post('/info')
async def get_data(file: UploadFile, job: str = Form(...)):
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
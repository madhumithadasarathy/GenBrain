from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from genbrain_core.engine import process_note, load_notes
from genbrain_core.file_parser import extract_text_from_file

app = FastAPI(title="GenBrain API", description="AI-powered notetaking assistant backend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NoteInput(BaseModel):
    text: str

class RelatedNote(BaseModel):
    text: str
    summary: str
    score: float

class NoteOutput(BaseModel):
    timestamp: str
    text: str
    summary: str
    tags: List[str]
    questions: List[str]
    related_notes: List[RelatedNote]

@app.get("/notes", response_model=List[NoteOutput])
async def get_all_notes():
    """Retrieve all processed notes."""
    try:
        return load_notes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process", response_model=NoteOutput)
async def process_new_note(input_data: NoteInput):
    """Process a new note: summarize, tag, and link."""
    try:
        if not input_data.text.strip():
            raise HTTPException(status_code=400, detail="Note text cannot be empty")
        
        result = process_note(input_data.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload", response_model=NoteOutput)
async def upload_file(file: UploadFile = File(...)):
    """Upload and process a document (PDF, TXT, MD)."""
    try:
        content = await file.read()
        text = extract_text_from_file(content, file.filename)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Extracted text is empty")
        
        result = process_note(text)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

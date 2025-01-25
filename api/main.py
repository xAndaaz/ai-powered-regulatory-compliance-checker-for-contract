# api/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from PyPDF2 import PdfReader
from app.database.vector_store import VectorStore  # Updated import path
from app.services.synthesizer import Synthesizer  # Import the Synthesizer class

app = FastAPI()

# Initialize VectorStore and Synthesizer
vec = VectorStore()
synthsizer = Synthesizer()


class AnalysisResponse(BaseModel):
    message: str
    pdf_path: str

def extract_text_from_pdf(pdf_file: UploadFile) -> str:
    """
    Extracts text from a PDF file.
    """
    try:
        reader = PdfReader(pdf_file.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text from PDF: {str(e)}")

@app.post("/analyze-contract/", response_model=AnalysisResponse)
async def analyze_contract(pdf_file: UploadFile = File(...)):
    """
    Analyzes a contract PDF and generates a suitability report.
    """
    try:
        # Step 1: Extract text from the PDF
        relevant_question = extract_text_from_pdf(pdf_file)

        # Step 2: Perform similarity search
        results = vec.search(relevant_question, limit=3)
        # Step 3: Generate response
        response = synthsizer.generate_response(question=relevant_question, context=results)

        # Step 4: Generate PDF report
        pdf_filename = "suitability_report.pdf"
        from app.similarity_search import convert_to_paragraphs  # Import the PDF generation function
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate

        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        paragraphs = convert_to_paragraphs(response.answer)
        doc.build(paragraphs)

        # Step 5: Return the PDF file
        if not os.path.exists(pdf_filename):
            raise HTTPException(status_code=500, detail="Failed to generate PDF report.")

        return AnalysisResponse(
            message="Analysis completed successfully.",
            pdf_path=pdf_filename,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/download-report/")
async def download_report(pdf_path: str):
    """
    Downloads the generated PDF report.
    """
    if not os.path.exists(pdf_path):
        raise HTTPException
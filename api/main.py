# api/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from PyPDF2 import PdfReader
from app.database.vector_store import VectorStore  # Updated import path
from app.services.synthesizer import Synthesizer  # Import the Synthesizer class
from typing import List

app = FastAPI()

# Initialize VectorStore and Synthesizer
vec = VectorStore()
synthsizer = Synthesizer()

class AnalysisResponse(BaseModel):
    message: str
    pdf_paths: List[str]

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

@app.post("/analyze-contracts/", response_model=AnalysisResponse)
async def analyze_contracts(pdf_files: List[UploadFile] = File(...)):
    """
    Analyzes multiple contract PDFs and generates suitability reports.
    """
    try:
        output_dir = "output_reports"
        os.makedirs(output_dir, exist_ok=True)
        pdf_paths = []

        for pdf_file in pdf_files:
            # Step 1: Extract text from the PDF
            relevant_question = extract_text_from_pdf(pdf_file)

            # Step 2: Perform similarity search
            results = vec.search(relevant_question, limit=3)

            # Step 3: Generate response
            response = synthsizer.generate_response(question=relevant_question, context=results)

            # Step 4: Generate PDF report
            pdf_filename = os.path.join(output_dir, f"{pdf_file.filename}_suitability_report.pdf")
            from app.similarity_search import convert_to_paragraphs  # Import the PDF generation function
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate

            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            paragraphs = convert_to_paragraphs(response.answer)
            doc.build(paragraphs)

            if not os.path.exists(pdf_filename):
                raise HTTPException(status_code=500, detail=f"Failed to generate PDF report for {pdf_file.filename}.")

            pdf_paths.append(pdf_filename)

        return AnalysisResponse(
            message="Analysis completed successfully for all contracts.",
            pdf_paths=pdf_paths,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/download-report/")
async def download_report(pdf_path: str):
    """
    Downloads the generated PDF report.
    """
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Report not found.")
    return FileResponse(pdf_path, media_type='application/pdf', filename=os.path.basename(pdf_path))
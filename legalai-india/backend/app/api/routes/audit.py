from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_parser import extract_text
from app.services.claude_service import analyze_compliance
from app.services.compliance_engine import load_rules_context

router = APIRouter()

@router.post("/audit")
async def run_audit(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are accepted")

    policy_text = await extract_text(file)

    if len(policy_text.strip()) < 100:
        raise HTTPException(400, "Could not extract readable text from this PDF")

    rules_context = load_rules_context()
    result = await analyze_compliance(policy_text, rules_context)

    return {
        "status": "success",
        "filename": file.filename,
        "analysis": result
    }

@router.get("/health")
def health():
    return {"status": "ok", "message": "Labour Code Compliance Engine is running"}
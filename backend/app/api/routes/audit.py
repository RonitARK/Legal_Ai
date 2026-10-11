from fastapi import Request
from fastapi.responses import StreamingResponse
import io
from app.services.report_generator import generate_audit_report
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

@router.post("/audit/report-from-result")
async def report_from_result(request: Request):
    from datetime import datetime
    import io
    from fastapi.responses import StreamingResponse
    from app.services.report_generator import generate_audit_report

    body = await request.json()

    # remap field names to match report_generator expectations
    gaps = []
    for g in body.get("gaps", []):
        gaps.append({
            "section":  g.get("section", ""),
            "issue":    g.get("issue", ""),
            "severity": g.get("severity", "high"),
            "fix":      g.get("compliant_text", g.get("fix", "")),
        })

    audit_data = {
        "overall_score": body.get("overall_score", body.get("score", 0)),
        "summary":       body.get("summary", ""),
        "gaps":          gaps,
    }

    pdf_bytes = generate_audit_report(audit_data, company_name="HR Policy Audit")
    filename  = f"legalai-compliance-report-{datetime.now().strftime('%Y%m%d-%H%M')}.pdf"

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
 
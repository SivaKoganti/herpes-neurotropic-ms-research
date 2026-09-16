from app.models.schemas import ReportRequest


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def generate_pdf_bytes(request: ReportRequest) -> bytes:
    lines = [
        f"MS Risk Report: {request.patient_id}",
        f"Risk Score: {request.risk_result.risk_score}",
        f"Severity: {request.risk_result.severity}",
        f"Credible Interval: {request.risk_result.credible_interval}",
    ]
    if request.notes:
        lines.append(f"Notes: {request.notes}")

    content = "\n".join(lines)
    escaped = _pdf_escape(content)
    stream = f"BT /F1 12 Tf 72 750 Td ({escaped}) Tj ET"

    pdf = (
        "%PDF-1.4\n"
        "1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n"
        "2 0 obj<< /Type /Pages /Count 1 /Kids [3 0 R] >>endobj\n"
        "3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>endobj\n"
        "4 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj\n"
        f"5 0 obj<< /Length {len(stream)} >>stream\n{stream}\nendstream endobj\n"
        "xref\n0 6\n0000000000 65535 f \n"
        "0000000010 00000 n \n0000000063 00000 n \n0000000120 00000 n \n"
        "0000000246 00000 n \n0000000316 00000 n \n"
        "trailer<< /Size 6 /Root 1 0 R >>\nstartxref\n420\n%%EOF"
    )
    return pdf.encode("utf-8")

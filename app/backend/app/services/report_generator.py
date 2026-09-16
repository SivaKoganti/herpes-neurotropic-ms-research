import textwrap

from app.models.schemas import ReportRequest


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def generate_pdf_bytes(request: ReportRequest) -> bytes:
    lines = [
        f"MS Risk Report: {request.patient_id}",
        f"Risk Score: {request.risk_result.risk_score}",
        f"Severity: {request.risk_result.severity}",
        f"Credible Interval: {request.risk_result.credible_interval}",
        "Research/decision-support output only; not for clinical diagnosis.",
    ]
    if request.notes:
        wrapped_notes = textwrap.wrap(request.notes, width=90) or [request.notes]
        lines.extend(["Notes:"] + wrapped_notes)

    escaped_lines = [_pdf_escape(line) for line in lines]
    line_ops = " T* ".join(f"({line}) Tj" for line in escaped_lines)
    stream = f"BT /F1 12 Tf 72 750 Td {line_ops} ET"

    objects = [
        "1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n",
        "2 0 obj<< /Type /Pages /Count 1 /Kids [3 0 R] >>endobj\n",
        "3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>endobj\n",
        "4 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj\n",
        f"5 0 obj<< /Length {len(stream.encode('utf-8'))} >>stream\n{stream}\nendstream endobj\n",
    ]

    pdf_chunks = ["%PDF-1.4\n"]
    offsets = [0]
    for obj in objects:
        offsets.append(sum(len(chunk.encode("utf-8")) for chunk in pdf_chunks))
        pdf_chunks.append(obj)

    xref_start = sum(len(chunk.encode("utf-8")) for chunk in pdf_chunks)
    xref_lines = ["xref\n0 6\n", "0000000000 65535 f \n"]
    xref_lines.extend(f"{offset:010d} 00000 n \n" for offset in offsets[1:])
    trailer = f"trailer<< /Size 6 /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF"

    return "".join(pdf_chunks + xref_lines + [trailer]).encode("utf-8")

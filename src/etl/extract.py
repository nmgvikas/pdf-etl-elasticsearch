import os
import re
import pdfplumber
from typing import Dict, List, Iterable

def _split_paragraphs(text: str) -> List[str]:
    if not text:
        return []
    # split on blank lines; trim; collapse inner whitespace
    paras = [re.sub(r"\s+", " ", p.strip()) for p in re.split(r"\n\s*\n+", text) if p and p.strip()]
    return paras

def _extract_tables(page) -> List[Dict]:
    tables_out = []
    try:
        tables = page.extract_tables() or []
        for tbl in tables:
            rows = []
            for row in tbl:
                if not row:
                    continue
                rows.append([(c or "").strip() for c in row])
            table_text = "\n".join(" | ".join(r) for r in rows) if rows else ""
            tables_out.append({"rows": rows, "table_text": table_text})
    except Exception:
        pass
    return tables_out

def _extract_images(page) -> List[Dict]:
    images = []
    try:
        for img in (page.images or []):
            x0 = float(img.get("x0", 0)); y0 = float(img.get("y0", 0))
            x1 = float(img.get("x1", 0)); y1 = float(img.get("y1", 0))
            images.append({
                "x0": x0, "y0": y0, "x1": x1, "y1": y1,
                "width": x1 - x0, "height": y1 - y0,
                "name": img.get("name")
            })
    except Exception:
        pass
    return images

def extract_pdf_pages(pdf_path: str) -> Iterable[Dict]:
    """Yield one page document per page with paragraphs, tables, images."""
    pdf_name = os.path.basename(pdf_path)
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            yield {
                "_id": f"{pdf_name}#p{i}",
                "pdf_name": pdf_name,
                "pdf_path": pdf_path,
                "page_number": i,
                "paragraphs": _split_paragraphs(text),
                "tables": _extract_tables(page),
                "images": _extract_images(page),
            }

def extract_from_dir(input_dir: str) -> List[Dict]:
    """Return list of all page docs for all PDFs in a directory."""
    docs: List[Dict] = []
    for name in os.listdir(input_dir):
        if not name.lower().endswith(".pdf"):
            continue
        path = os.path.join(input_dir, name)
        for page_doc in extract_pdf_pages(path):
            docs.append(page_doc)
    return docs

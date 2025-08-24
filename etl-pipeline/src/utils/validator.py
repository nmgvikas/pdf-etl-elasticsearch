from typing import Dict, List

def validate_page_doc(doc: Dict) -> List[str]:
    """Return list of validation errors (empty = valid)."""
    errors = []
    required = ["pdf_name", "pdf_path", "page_number", "paragraphs", "tables", "images"]
    for k in required:
        if k not in doc:
            errors.append(f"missing field: {k}")
    if "page_number" in doc and not isinstance(doc["page_number"], int):
        errors.append("page_number must be int")
    if "paragraphs" in doc and not isinstance(doc["paragraphs"], list):
        errors.append("paragraphs must be list[str]")
    return errors

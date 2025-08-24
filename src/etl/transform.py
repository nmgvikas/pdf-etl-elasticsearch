from typing import Dict, List

def normalize_doc(doc: Dict) -> Dict:
    """Light transform hook: currently passthrough (already normalized in extract).
       You can enrich here (e.g., add page_text_len, paragraph_count, etc.)."""
    d = dict(doc)
    d["paragraph_count"] = len(d.get("paragraphs", []))
    d["table_count"] = len(d.get("tables", []))
    d["image_count"] = len(d.get("images", []))
    return d

def transform_batch(docs: List[Dict]) -> List[Dict]:
    return [normalize_doc(d) for d in docs]

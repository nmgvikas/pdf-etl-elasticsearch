from typing import Any, Dict, List, Optional
from elasticsearch import Elasticsearch
from config import ES_HOST

# Keep ES v8-compatible headers (avoids version negotiation errors on some clusters)
_COMPAT_HEADERS = {
    "Accept": "application/vnd.elasticsearch+json; compatible-with=8",
    "Content-Type": "application/vnd.elasticsearch+json; compatible-with=8",
}

# Local ES (no auth)
_es: Optional[Elasticsearch] = None
def get_es() -> Elasticsearch:
    global _es
    if _es is None:
        _es = Elasticsearch(
            ES_HOST,
            headers=_COMPAT_HEADERS,
            request_timeout=30,
            verify_certs=False,  # set True + CA in prod
        )
    return _es

def search_paragraphs(
    index: str,
    q: str,
    page_from: Optional[int] = None,
    page_to: Optional[int] = None,
    size: int = 10
) -> List[Dict[str, Any]]:
    """
    Searches the 'paragraphs' array field in your per-page docs.
    Optionally filters by page range if your docs have 'page_number'.
    """
    es = get_es()

    must = [{"match": {"paragraphs": {"query": q}}}]
    filters: List[Dict[str, Any]] = []

    # If your ETL stored a different field name (e.g., 'page_num' or 'page_index'),
    # change 'page_number' below to match.
    if page_from is not None or page_to is not None:
        range_body: Dict[str, Any] = {"range": {"page_number": {}}}
        if page_from is not None:
            range_body["range"]["page_number"]["gte"] = page_from
        if page_to is not None:
            range_body["range"]["page_number"]["lte"] = page_to
        filters.append(range_body)

    body = {
        "query": {
            "bool": {
                "must": must,
                "filter": filters
            }
        },
        "_source": ["file_name", "page_number", "paragraphs"],
        "highlight": {
            "fields": {
                "paragraphs": {
                    "fragment_size": 160,
                    "number_of_fragments": 3
                }
            }
        },
        "size": size
    }

    # Using 'body' keeps it simple and works with the 8.x client.
    resp = es.search(index=index, body=body)

    hits = []
    for h in resp.get("hits", {}).get("hits", []):
        src = h.get("_source", {})
        hits.append({
            "id": h.get("_id"),
            "score": h.get("_score"),
            "file_name": src.get("file_name"),
            "page_number": src.get("page_number"),
            "highlights": h.get("highlight", {}).get("paragraphs", []),
            # Uncomment below if you want to return full paragraphs too
            # "paragraphs": src.get("paragraphs", []),
        })
    return hits

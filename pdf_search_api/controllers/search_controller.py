from fastapi import APIRouter, Query, Depends
from typing import Optional
from config import ES_INDEX
from repositories.es_repository import search_paragraphs
from auth import get_current_user

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/paragraphs")
def search_paragraphs_endpoint(
    q: str = Query(..., description="Your search query"),
    index: str = Query(ES_INDEX, description="Elasticsearch index name"),
    page_from: Optional[int] = Query(None, description="Start page (inclusive)"),
    page_to: Optional[int] = Query(None, description="End page (inclusive)"),
    size: int = Query(10, ge=1, le=100),
    current_user: str = Depends(get_current_user)   # expects Authorization: Bearer <JWT>
):
    """
    Searches only 'paragraphs' in the per-page ES index.
    """
    results = search_paragraphs(
        index=index,
        q=q,
        page_from=page_from,
        page_to=page_to,
        size=size
    )
    return {"count": len(results), "results": results}

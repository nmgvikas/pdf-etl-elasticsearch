import json
from typing import List, Dict
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.helpers.errors import BulkIndexError

DEFAULT_MAPPING = {
    "mappings": {
        "properties": {
            "pdf_name":   {"type": "keyword"},
            "pdf_path":   {"type": "keyword"},
            "page_number":{"type": "integer"},
            "paragraphs": {"type": "text"},
            "paragraph_count": {"type": "integer"},
            "table_count": {"type": "integer"},
            "image_count": {"type": "integer"},
            "tables": {
                "type": "nested",
                "properties": {
                    "table_text": {"type": "text"},
                    "rows": {"type": "object", "enabled": False}
                }
            },
            "images": {
                "type": "nested",
                "properties": {
                    "x0": {"type": "float"},
                    "y0": {"type": "float"},
                    "x1": {"type": "float"},
                    "y1": {"type": "float"},
                    "width": {"type": "float"},
                    "height": {"type": "float"},
                    "name": {"type": "keyword"}
                }
            }
        }
    }
}

def get_es(url: str) -> Elasticsearch:
    # If your ES requires auth/SSL, add it here (basic_auth=..., verify_certs=...)
    return Elasticsearch(url)

def ensure_index(es: Elasticsearch, index_name: str):
    if es.indices.exists(index=index_name):
        return
    es.indices.create(index=index_name, body=DEFAULT_MAPPING)

def index_pages(es: Elasticsearch, index_name: str, docs: List[Dict], logger):
    if not docs:
        logger.info("No documents to index.")
        return
    actions = [
        {
            "_op_type": "index",           # upsert by _id on ES 8+
            "_index": index_name,
            "_id": d["_id"],
            "_source": {k: v for k, v in d.items() if k != "_id"}
        }
        for d in docs
    ]
    try:
        bulk(es, actions, refresh="wait_for")
        logger.info(f"Indexed {len(actions)} page docs into '{index_name}'.")
    except BulkIndexError as e:
        logger.error("Bulk indexing errors:")
        for err in e.errors[:5]:
            logger.error(json.dumps(err, indent=2))

def count_docs(es: Elasticsearch, index_name: str) -> int:
    try:
        # new-style param 'query' to avoid deprecation warnings
        res = es.count(index=index_name, query={"match_all": {}})
        return res.get("count", 0)
    except Exception:
        return 0

from typing import List, Dict
from ..utils.logger import get_logger
from ..utils.config import load_config
from ..utils.validator import validate_page_doc
from .extract import extract_from_dir
from .transform import transform_batch
from .load import get_es, ensure_index, index_pages, count_docs

logger = get_logger("etl.pipeline")

def run_pipeline(config_path: str = "config/config.yaml"):
    cfg = load_config(config_path)
    input_dir = cfg["paths"]["input_dir"]
    index_name = cfg["elasticsearch"]["index"]
    es_url = cfg["elasticsearch"]["url"]

    logger.info(f"Starting ETL | input_dir={input_dir} index={index_name} es={es_url}")

    # Extract
    raw_docs: List[Dict] = extract_from_dir(input_dir)
    logger.info(f"Extracted {len(raw_docs)} page docs")

    # Validate
    invalid = []
    for d in raw_docs:
        errs = validate_page_doc(d)
        if errs:
            invalid.append((d.get('_id'), errs))
    if invalid:
        logger.warning(f"{len(invalid)} page docs failed validation; they will be skipped")
        raw_docs = [d for d in raw_docs if not validate_page_doc(d)]

    # Transform
    docs = transform_batch(raw_docs)
    logger.info("Transform complete")

    # Load
    es = get_es(es_url)
    ensure_index(es, index_name)
    index_pages(es, index_name, docs, logger)

    total = count_docs(es, index_name)
    logger.info(f"Pipeline finished. Index '{index_name}' now has {total} documents.")

import os

# Point this at your running ES. For Docker Desktop defaults, use http://localhost:9200
ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")

# Default index created by your ETL (change if yours differs)
ES_INDEX = os.getenv("ES_INDEX", "pdf_documents")

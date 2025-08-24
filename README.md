# PDF ETL → Elasticsearch (per-page, paragraphs/tables/images)

This ETL parses PDFs **per page**, extracts:
- `paragraphs: string[]`
- `tables: [{ rows: string[][], table_text: string }]`
- `images: [{ x0,y0,x1,y1,width,height,name }]`
…and bulk-indexes into Elasticsearch (one document per page).

## Quickstart

1) Install deps (match ES client to your server):
```bash
pip install -r requirements.txt
```

2) Run the ETL:

```bash
python -m src.main <path-to-pdf>
```

## Running Elasticsearch in Docker

You’ll need Elasticsearch running before using this ETL.

Start Elasticsearch (single-node mode) via Docker:

```bash
docker run -d --name es \
  -p 9200:9200 \
  -e "discovery.type=single-node" \
  docker.elastic.co/elasticsearch/elasticsearch:8.13.4
```

Verify it’s running:

```bash
curl http://localhost:9200
```

You should see cluster details returned as JSON.

## Searching the Indexed Data

Once documents are indexed, you can search them.

1. **Match all pages**
    ```bash
    curl -X GET "http://localhost:9200/pdf_index/_search?pretty" \
      -H 'Content-Type: application/json' \
      -d '{"query": {"match_all": {}}}'
    ```

2. **Search within paragraphs**
    ```bash
    curl -X GET "http://localhost:9200/pdf_index/_search?pretty" \
      -H 'Content-Type: application/json' \
      -d '{"query": {"match": {"paragraphs": "your keyword"}}}'
    ```

3. **Search within tables**
    ```bash
    curl -X GET "http://localhost:9200/pdf_index/_search?pretty" \
      -H 'Content-Type: application/json' \
      -d '{"query": {"match": {"tables.table_text": "your keyword"}}}'
    ```

4. **Combine filters (paragraphs + tables)**
    ```bash
    curl -X GET "http://localhost:9200/pdf_index/_search?pretty" \
      -H 'Content-Type: application/json' \
      -d '{
        "query": {
          "bool": {
            "should": [
              { "match": { "paragraphs": "your keyword" }},
              { "match": { "tables.table_text": "your keyword" }}
            ]
          }
        }
      }'
    ```

5. **Count matches quickly**
    ```bash
    curl -X GET "http://localhost:9200/pdf_index/_count" \
      -H 'Content-Type: application/json' \
      -d '{"query": {"match": {"paragraphs": "your keyword"}}}'
    ```

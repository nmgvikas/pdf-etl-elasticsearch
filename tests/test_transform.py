from etl.transform import normalize_doc

def test_normalize_counts():
    d = {
        "pdf_name": "a.pdf", "pdf_path": "/a.pdf", "page_number": 1,
        "paragraphs": ["x"], "tables": [{"rows":[["a"]], "table_text":"a"}], "images":[{}]
    }
    out = normalize_doc(d)
    assert out["paragraph_count"] == 1
    assert out["table_count"] == 1
    assert out["image_count"] == 1

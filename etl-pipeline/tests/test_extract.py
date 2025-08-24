from etl.extract import _split_paragraphs

def test_split_paragraphs_basic():
    s = "Para one.\n\nPara two.\n\n\nPara three."
    paras = _split_paragraphs(s)
    assert paras == ["Para one.", "Para two.", "Para three."]

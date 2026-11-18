from services.text_preprocessing import TextPreprocessor
def test_cleaning():
    result=TextPreprocessor().preprocess("Researchers are testing ML models at https://example.com")
    assert "researchers" in result["tokens"]
    assert "http" not in result["processed_text"]

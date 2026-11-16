from src.features import extract_features, explain_url

def test_feature_extraction_returns_expected_keys():
    result = extract_features("https://example.com/login")
    assert result["has_https_scheme"] == 1
    assert result["suspicious_word_count"] >= 1
    assert "url_length" in result

def test_ip_address_is_detected():
    result = extract_features("http://192.168.1.10/login")
    assert result["has_ip_address"] == 1

def test_explanation_is_not_empty():
    assert explain_url("http://example.com") 

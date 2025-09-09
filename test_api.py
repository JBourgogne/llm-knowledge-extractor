# Simple API tests for the LLM Knowledge Extractor // Run with: python test_api.py
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    print("Health check passed")

def test_analyze_text():
    """Test text analysis endpoint"""
    test_text = """
    Apple announced groundbreaking AI features in their latest iPhone lineup. 
    The technology giant continues to innovate in mobile computing and artificial intelligence.
    This marks a significant shift in their product strategy.
    """
    
    response = requests.post(
        f"{BASE_URL}/analyze",
        json={"text": test_text}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "id" in data
    assert "summary" in data
    assert "metadata" in data
    
    metadata = data["metadata"]
    assert "title" in metadata
    assert "topics" in metadata and len(metadata["topics"]) == 3
    assert "sentiment" in metadata
    assert "keywords" in metadata and len(metadata["keywords"]) == 3
    
    print(f"Analysis passed: {data['summary'][:50]}...")
    return data["id"]

def test_empty_input():
    """Test that empty input is rejected"""
    response = requests.post(
        f"{BASE_URL}/analyze",
        json={"text": ""}
    )
    assert response.status_code == 400
    print("Empty input validation passed")

def test_search(topic="technology"):
    """Test search functionality"""
    response = requests.get(f"{BASE_URL}/search?topic={topic}")
    assert response.status_code == 200
    results = response.json()
    print(f"Search passed: Found {len(results)} results for '{topic}'")

def test_batch_processing():
    """Test batch processing endpoint"""
    texts = [
        {"text": "First article about technology and innovation."},
        {"text": "Second article about business and markets."},
        {"text": ""}  # Include empty to test error handling
    ]
    
    response = requests.post(
        f"{BASE_URL}/analyze_batch",
        json=texts
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "successful" in data
    assert "errors" in data
    assert data["total_processed"] == 2
    assert data["total_errors"] == 1
    print(f"Batch processing passed: {data['total_processed']} successful, {data['total_errors']} errors")

if __name__ == "__main__":
    print("Running API tests...\n")
    
    try:
        # Check if server is running
        requests.get(BASE_URL, timeout=1)
    except:
        print("Server not running! Start with: uvicorn app.main:app --reload")
        exit(1)
    
    test_health_check()
    test_empty_input()
    analysis_id = test_analyze_text()
    test_search()
    test_batch_processing()
    
    print("All tests passed!")
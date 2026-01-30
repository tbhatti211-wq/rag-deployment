"""
API Tests for RAG Deployment - Fast Test Suite
Tests all critical API endpoints and functionality
"""

import pytest
import requests
import json
import time

# Test configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 30  # seconds


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_json(self):
        """Test /health endpoint returns JSON"""
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "rag_system" in data
        print("✅ Health check JSON working")
    
    def test_health_ui(self):
        """Test /health-ui endpoint returns HTML"""
        response = requests.get(f"{BASE_URL}/health-ui", timeout=5)
        assert response.status_code == 200
        assert "text/html" in response.headers.get("Content-Type", "")
        print("✅ Health check UI working")


class TestAskEndpoint:
    """Test the main /ask endpoint"""
    
    def test_ask_technical_question(self):
        """Test technical question gets RAG response"""
        payload = {"question": "What is machine learning?"}
        response = requests.post(f"{BASE_URL}/ask", json=payload, timeout=TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "answer" in data
        assert "question_type" in data
        assert data["question_type"] == "technical"
        assert "sources" in data
        assert len(data["sources"]) > 0
        print(f"✅ Technical question: {data['question_type']}, {len(data['sources'])} sources")
    
    def test_ask_general_question(self):
        """Test general question gets conversational response"""
        payload = {"question": "Hello, how are you?"}
        response = requests.post(f"{BASE_URL}/ask", json=payload, timeout=TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "answer" in data
        assert "question_type" in data
        assert data["question_type"] == "general"
        print(f"✅ General question: {data['question_type']}")
    
    def test_ask_without_question(self):
        """Test error handling for missing question"""
        payload = {}
        response = requests.post(f"{BASE_URL}/ask", json=payload, timeout=5)
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        print("✅ Error handling working")
    
    def test_ask_empty_question(self):
        """Test error handling for empty question"""
        payload = {"question": ""}
        response = requests.post(f"{BASE_URL}/ask", json=payload, timeout=5)
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        print("✅ Empty question validation working")
    
    def test_ask_multiple_questions(self):
        """Test multiple sequential questions"""
        questions = [
            "What is deep learning?",
            "Explain neural networks",
            "What is supervised learning?"
        ]
        
        for q in questions:
            payload = {"question": q}
            response = requests.post(f"{BASE_URL}/ask", json=payload, timeout=TIMEOUT)
            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            time.sleep(0.5)  # Small delay between requests
        
        print(f"✅ Multiple questions ({len(questions)}) working")


class TestWebInterface:
    """Test web interface is accessible"""
    
    def test_index_page(self):
        """Test main page loads"""
        response = requests.get(f"{BASE_URL}/", timeout=5)
        assert response.status_code == 200
        assert "text/html" in response.headers.get("Content-Type", "")
        assert b"RAG Assistant" in response.content or b"Chat" in response.content
        print("✅ Web interface loading")


class TestPerformance:
    """Basic performance tests"""
    
    def test_response_time(self):
        """Test response time is acceptable"""
        payload = {"question": "What is AI?"}
        
        start = time.time()
        response = requests.post(f"{BASE_URL}/ask", json=payload, timeout=TIMEOUT)
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < TIMEOUT
        print(f"✅ Response time: {elapsed:.2f}s")


def run_all_tests():
    """Run all tests and display results"""
    print("\n" + "="*60)
    print("🧪 RAG API Test Suite - Fast Mode")
    print("="*60 + "\n")
    
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=2)
    except requests.exceptions.ConnectionError:
        print("❌ Server not running! Start with: bash deploy.sh")
        return False
    
    print("✅ Server is running\n")
    
    test_classes = [
        TestHealthEndpoints(),
        TestAskEndpoint(),
        TestWebInterface(),
        TestPerformance()
    ]
    
    total = 0
    passed = 0
    failed = 0
    
    for test_class in test_classes:
        class_name = test_class.__class__.__name__
        print(f"\n📋 {class_name}")
        print("-" * 40)
        
        for method_name in dir(test_class):
            if method_name.startswith("test_"):
                total += 1
                try:
                    method = getattr(test_class, method_name)
                    method()
                    passed += 1
                except AssertionError as e:
                    failed += 1
                    print(f"❌ {method_name}: {str(e)}")
                except Exception as e:
                    failed += 1
                    print(f"❌ {method_name}: {type(e).__name__}: {str(e)}")
    
    print("\n" + "="*60)
    print(f"📊 Results: {passed}/{total} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

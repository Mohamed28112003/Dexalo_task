# test_api.py
import requests
import os

# API endpoint
BASE_URL = "http://localhost:8000"

def test_upload_file():
    """Test uploading a file to the API"""
    # Path to your test file
    test_file_path = "test_document.txt"  # Adjust this to your test file
    
    # Check if file exists
    if not os.path.exists(test_file_path):
        print(f"Creating test file: {test_file_path}")
        with open(test_file_path, "w") as f:
            f.write("This is a test document about Dexalo company. Dexalo is a technology company specializing in AI solutions.")
    
    # Upload the file
    files = {"files": open(test_file_path, "rb")}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    
    print("Upload Response:", response.status_code)
    print(response.json())
    
    return response.status_code == 200

def test_query():
    """Test querying the API"""
    query = "What is dexalo company?"
    
    response = requests.post(
        f"{BASE_URL}/query",
        json={"query": query}
    )
    
    print("\nQuery Response:", response.status_code)
    if response.status_code == 200:
        result = response.json()
        print(f"Question: {result['query']}")
        print(f"Answer: {result['answer']}")
        print(f"Processing Time: {result['processing_time']} seconds")
        if result.get('sources'):
            print("Sources:")
            for source in result['sources']:
                print(f"- {source}")
    else:
        print("Error:", response.json())
    
    return response.status_code == 200

def test_list_documents():
    """Test listing all documents"""
    response = requests.get(f"{BASE_URL}/documents")
    
    print("\nList Documents Response:", response.status_code)
    print(response.json())
    
    return response.status_code == 200

if __name__ == "__main__":
    print("Starting API tests...")
    
    # Run tests
    upload_successful = test_upload_file()
    if upload_successful:
        test_query()
        test_list_documents()
    else:
        print("Upload failed, skipping other tests")
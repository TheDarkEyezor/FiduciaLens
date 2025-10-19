"""
Test Document Verification System
Uploads sample documents and verifies signature validation
"""

import json
import requests
import base64

# Test wallet address (replace with your actual test address)
TEST_ADDRESS = "YOUR_ALGORAND_ADDRESS_HERE"

def load_sample_documents():
    """Load generated sample documents"""
    with open("sample_documents.json", "r") as f:
        data = json.load(f)
    return data["documents"]

def test_document_upload(document, base_url="http://localhost:8000"):
    """Test uploading a document to the API"""
    
    # Encode content to base64
    content_base64 = base64.b64encode(document["content"].encode()).decode()
    
    payload = {
        "address": TEST_ADDRESS,
        "document_type": document["document_type"],
        "content": content_base64,
        "issuer_id": document["issuer_id"],
        "issuer_signature": document["issuer_signature"]
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/documents/upload",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else response.text,
            "expected_valid": document["valid"]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "expected_valid": document["valid"]
        }

def run_tests():
    """Run all document verification tests"""
    print("=" * 80)
    print("DOCUMENT VERIFICATION SYSTEM TESTS")
    print("=" * 80)
    print()
    
    if TEST_ADDRESS == "YOUR_ALGORAND_ADDRESS_HERE":
        print("⚠️  WARNING: Update TEST_ADDRESS with your actual Algorand address!")
        print("   Using placeholder address for demonstration...\n")
    
    documents = load_sample_documents()
    
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "details": []
    }
    
    for i, doc in enumerate(documents, 1):
        doc_type = doc["document_type"]
        is_valid = doc["valid"]
        status_icon = "✅" if is_valid else "❌"
        
        print(f"\n{'='*80}")
        print(f"Test {i}/{len(documents)}: {doc_type.upper()} - {status_icon} {'VALID' if is_valid else 'INVALID'} SIGNATURE")
        print(f"{'='*80}")
        print(f"Issuer: {doc['issuer_id']}")
        print(f"Hash: {doc['document_hash'][:64]}...")
        print(f"Signature: {doc['issuer_signature'][:64]}...")
        print()
        
        result = test_document_upload(doc)
        results["total"] += 1
        
        # Validate result
        if is_valid:
            # Valid documents should be accepted (200)
            if result["success"]:
                print("✅ PASS: Valid document accepted")
                results["passed"] += 1
                if "response" in result:
                    resp = result["response"]
                    print(f"   Credit Boost: +{resp.get('credit_boost', 0)} points")
                    print(f"   Signature Valid: {resp.get('signature_valid', False)}")
            else:
                print(f"❌ FAIL: Valid document rejected (Status: {result.get('status_code')})")
                print(f"   Error: {result.get('response', result.get('error'))}")
                results["failed"] += 1
        else:
            # Invalid documents should be rejected (400)
            if not result["success"] and result.get("status_code") == 400:
                print("✅ PASS: Invalid document correctly rejected")
                results["passed"] += 1
                print(f"   Rejection reason: {result.get('response', 'Signature validation failed')}")
            else:
                print(f"❌ FAIL: Invalid document should be rejected (Status: {result.get('status_code')})")
                results["failed"] += 1
        
        results["details"].append({
            "document_type": doc_type,
            "expected_valid": is_valid,
            "test_passed": (is_valid and result["success"]) or (not is_valid and not result["success"]),
            "result": result
        })
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    print("=" * 80)
    
    # Expected behavior summary
    print("\n" + "=" * 80)
    print("EXPECTED BEHAVIOR")
    print("=" * 80)
    print("✅ Valid signatures (tests 1-6):")
    print("   - Should return 200 OK")
    print("   - Should include credit_boost value")
    print("   - signature_valid should be True")
    print()
    print("❌ Invalid signatures (tests 7-8):")
    print("   - Should return 400 Bad Request")
    print("   - Should reject with signature validation error")
    print("   - Should NOT add credit boost")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code != 200:
            print("⚠️  Backend health check failed. Is the server running?")
            print("   Start it with: uvicorn main:app --reload")
            exit(1)
    except:
        print("❌ Cannot connect to backend at http://localhost:8000")
        print("   Please start the backend server:")
        print("   cd backend && uvicorn main:app --reload")
        exit(1)
    
    results = run_tests()
    
    # Save test results
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n✅ Test results saved to test_results.json")
    
    # Exit with appropriate code
    exit(0 if results["failed"] == 0 else 1)

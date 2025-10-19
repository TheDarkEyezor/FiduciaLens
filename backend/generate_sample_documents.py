"""
Sample Document Generator for TrustLens Document Verification Testing
Creates valid and invalid documents with cryptographic signatures
"""

import hashlib
import hmac
import base64
import json
from datetime import datetime

# These must match the backend TRUSTED_ISSUERS
TRUSTED_ISSUERS = {
    "US_GOVT_PASSPORT": "demo_secret_govt_passport_2024",
    "US_DMV": "demo_secret_dmv_license_2024",
    "CHASE_BANK": "demo_secret_chase_bank_2024",
    "BOA": "demo_secret_boa_bank_2024",
    "WELLS_FARGO": "demo_secret_wells_fargo_2024",
    "IRS": "demo_secret_irs_tax_2024",
    "UTIL_COMPANY": "demo_secret_utility_2024",
    "DEMO_BANK": "demo_secret_bank_statement_2024",
    "DEMO_GOVT": "demo_secret_government_id_2024",
}

def create_signature(document_hash: str, issuer_id: str) -> str:
    """Create HMAC signature for a document"""
    if issuer_id not in TRUSTED_ISSUERS:
        raise ValueError(f"Unknown issuer: {issuer_id}")
    
    secret = TRUSTED_ISSUERS[issuer_id]
    signature = hmac.new(
        secret.encode(),
        document_hash.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature

def create_sample_document(doc_type: str, content: str, issuer_id: str, valid: bool = True):
    """
    Create a sample document with signature
    
    Args:
        doc_type: Type of document (passport, drivers_license, etc.)
        content: Document content (text or base64 encoded)
        issuer_id: Issuer ID (must be in TRUSTED_ISSUERS)
        valid: If False, creates an invalid signature
    """
    # Create document hash
    document_hash = hashlib.sha256(content.encode()).hexdigest()
    
    if valid:
        # Create valid signature
        signature = create_signature(document_hash, issuer_id)
    else:
        # Create invalid signature (random garbage)
        signature = "INVALID_" + hashlib.sha256(b"fake_signature").hexdigest()
    
    return {
        "document_type": doc_type,
        "content": content,
        "document_hash": document_hash,
        "issuer_id": issuer_id,
        "issuer_signature": signature,
        "valid": valid,
        "created_at": datetime.now().isoformat()
    }

# Generate sample documents
def generate_all_samples():
    samples = []
    
    # 1. VALID PASSPORT
    passport_content = """
PASSPORT
United States of America
Surname: DOE
Given Names: JOHN MICHAEL
Nationality: USA
Date of Birth: 15 JAN 1990
Sex: M
Place of Birth: NEW YORK, NY
Date of Issue: 01 JAN 2020
Date of Expiration: 01 JAN 2030
Passport No: 123456789
"""
    samples.append(create_sample_document(
        "passport",
        passport_content,
        "DEMO_GOVT",
        valid=True
    ))
    
    # 2. VALID DRIVER'S LICENSE
    license_content = """
DRIVER LICENSE
State: California
License No: D1234567
Name: JANE SARAH SMITH
DOB: 03/15/1985
Sex: F
Height: 5-06
Eyes: BRN
Address: 123 Main St, Los Angeles, CA 90001
Issue Date: 01/15/2023
Expiration: 01/15/2028
Class: C
"""
    samples.append(create_sample_document(
        "drivers_license",
        license_content,
        "US_DMV",
        valid=True
    ))
    
    # 3. VALID BANK STATEMENT
    bank_statement = """
CHASE BANK
Account Statement - December 2024

Account Holder: Robert Johnson
Account Number: ****5678
Statement Period: 12/01/2024 - 12/31/2024

Beginning Balance: $15,234.56
Total Deposits: $8,500.00
Total Withdrawals: $3,200.00
Ending Balance: $20,534.56

Average Balance: $18,000.00
Account Type: Checking
Account Status: Active - Good Standing
"""
    samples.append(create_sample_document(
        "bank_statement",
        bank_statement,
        "CHASE_BANK",
        valid=True
    ))
    
    # 4. VALID UTILITY BILL
    utility_bill = """
PACIFIC POWER & ELECTRIC
Bill Statement - January 2025

Service Address: 456 Oak Avenue, San Francisco, CA 94102
Account Number: 9876543210
Customer Name: Maria Garcia

Current Charges: $125.45
Due Date: 02/15/2025
Service Period: 12/15/2024 - 01/15/2025

Usage: 350 kWh
Account Status: Current
"""
    samples.append(create_sample_document(
        "utility_bill",
        utility_bill,
        "UTIL_COMPANY",
        valid=True
    ))
    
    # 5. VALID EMPLOYMENT VERIFICATION
    employment = """
TECHCORP INC.
Employment Verification Letter

Date: January 10, 2025

To Whom It May Concern,

This letter confirms that Michael Chen has been employed with TechCorp Inc. 
as a Senior Software Engineer since March 15, 2020.

Current Annual Salary: $145,000
Employment Status: Full-time, Active
Department: Engineering
Direct Supervisor: Jane Williams, VP Engineering

HR Contact: hr@techcorp.com | (555) 123-4567

Sincerely,
Human Resources Department
"""
    samples.append(create_sample_document(
        "employment_letter",
        employment,
        "DEMO_BANK",  # Using DEMO_BANK as stand-in for employment verification
        valid=True
    ))
    
    # 6. VALID TAX RETURN
    tax_return = """
U.S. Individual Income Tax Return
Form 1040 - 2023

Taxpayer: David Anderson
SSN: ***-**-1234
Filing Status: Single

Total Income: $95,000
Adjusted Gross Income: $90,000
Total Tax: $15,234
Federal Tax Withheld: $16,000
Refund: $766

IRS Processing Date: 04/15/2024
Return Status: Accepted
"""
    samples.append(create_sample_document(
        "tax_return",
        tax_return,
        "IRS",
        valid=True
    ))
    
    # 7. INVALID PASSPORT (wrong signature)
    fake_passport = """
PASSPORT
Democratic People's Republic of Fakeland
Surname: FRAUDSTER
Given Names: SCAM ARTIST
Nationality: FAKE
Date of Birth: 01 JAN 1900
Passport No: FAKE123456
"""
    samples.append(create_sample_document(
        "passport",
        fake_passport,
        "DEMO_GOVT",
        valid=False
    ))
    
    # 8. INVALID BANK STATEMENT (wrong signature)
    fake_bank = """
TOTALLY LEGIT BANK
Account Statement

Account Holder: Rich Person
Balance: $999,999,999.99
Status: Super Excellent
"""
    samples.append(create_sample_document(
        "bank_statement",
        fake_bank,
        "CHASE_BANK",
        valid=False
    ))
    
    return samples

if __name__ == "__main__":
    print("=" * 80)
    print("TRUSTLENS DOCUMENT VERIFICATION - SAMPLE DOCUMENTS")
    print("=" * 80)
    print()
    
    samples = generate_all_samples()
    
    for i, doc in enumerate(samples, 1):
        status = "✅ VALID" if doc["valid"] else "❌ INVALID"
        print(f"\n{i}. {doc['document_type'].upper()} - {status}")
        print(f"   Issuer: {doc['issuer_id']}")
        print(f"   Hash: {doc['document_hash'][:32]}...")
        print(f"   Signature: {doc['issuer_signature'][:32]}...")
        print()
    
    # Save to JSON file
    output = {
        "generated_at": datetime.now().isoformat(),
        "total_documents": len(samples),
        "valid_count": sum(1 for d in samples if d["valid"]),
        "invalid_count": sum(1 for d in samples if not d["valid"]),
        "documents": samples
    }
    
    with open("sample_documents.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("=" * 80)
    print(f"✅ Generated {len(samples)} sample documents")
    print(f"   Valid: {output['valid_count']}")
    print(f"   Invalid: {output['invalid_count']}")
    print(f"   Saved to: sample_documents.json")
    print("=" * 80)
    print()
    print("TESTING INSTRUCTIONS:")
    print("=" * 80)
    print("1. Valid documents (1-6) should be ACCEPTED by the backend")
    print("2. Invalid documents (7-8) should be REJECTED with signature error")
    print()
    print("To test via API:")
    print("  curl -X POST http://localhost:8000/api/documents/upload \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{")
    print('      "address": "YOUR_ALGO_ADDRESS",')
    print('      "document_type": "passport",')
    print('      "content": "BASE64_ENCODED_CONTENT",')
    print('      "issuer_id": "DEMO_GOVT",')
    print('      "issuer_signature": "SIGNATURE_FROM_JSON"')
    print("    }'")
    print("=" * 80)

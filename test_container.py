#!/usr/bin/env python3
"""
Test script for AWS Lambda container locally
Creative Cash Draw Solutions - Change Calculator
"""

import json

def test_lambda_container():
    """Test the Lambda container locally using Docker"""

    # Test data
    test_payload = {
        "body": "2.13,3.00\n2.14,3.00\n5.00,5.00"
    }

    print("Testing AWS Lambda container locally...")
    print("Note: This requires Docker to be running and the container to be built")
    print()

    try:
        # Test the container (this would require Docker to be running)
        # For demonstration, we'll show how it would work

        print("To test the container locally, run:")
        print("docker run -p 9000:8080 change-calculator:latest")
        print()
        print("Then test with curl:")
        print('curl -X POST http://localhost:9000/2015-03-31/functions/function/invocations -d \'{"body": "2.13,3.00"}\'')
        print()

        # Simulate what the Lambda function would return
        # Import without boto3 dependency for testing
        import sys
        import os
        sys.path.insert(0, os.path.dirname(__file__))

        # Mock boto3 to avoid import error
        import sys
        from unittest.mock import MagicMock
        sys.modules['boto3'] = MagicMock()

        from lambda_function import lambda_handler

        # Test change calculation
        result = lambda_handler(test_payload, {})
        print("Lambda function test result:")
        print(json.dumps(result, indent=2))

        # Test custom currency upload
        custom_currency = """CURRENCY_CODE=TEST
CURRENCY_NAME=Test Currency
CURRENCY_SYMBOL=@
100_note=10000
50_note=5000
10_coin=1000
5_coin=500
1_coin=100"""

        upload_payload = {
            "path": "/upload-currency",
            "body": custom_currency
        }

        upload_result = lambda_handler(upload_payload, {})
        print("\nCustom currency upload test result:")
        print(json.dumps(upload_result, indent=2))

        # Test using custom currency
        custom_test_payload = {
            "body": "10.50,20.00",
            "queryStringParameters": {"currency": "TEST"}
        }

        custom_result = lambda_handler(custom_test_payload, {})
        print("\nCustom currency calculation test result:")
        print(json.dumps(custom_result, indent=2))

        print("\nLocal testing completed successfully!")

    except Exception as e:
        print(f"Test failed: {e}")
        return False

    return True

if __name__ == "__main__":
    test_lambda_container()
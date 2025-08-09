#!/usr/bin/env python3
import requests
import json

def test_endpoint(url, name):
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            data = response.json()
            print(f"✓ {name}: Success - {data['count']} items collected")
            return True
        else:
            print(f"✗ {name}: Failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ {name}: Error - {e}")
        return False

def main():
    base_url = "http://127.0.0.1:8888/api"
    endpoints = [
        (f"{base_url}/crypto-news", "Crypto News API"),
        (f"{base_url}/crypto-market", "Crypto Market API"),
        (f"{base_url}/crunchbase-crypto", "Crunchbase Crypto API")
    ]
    
    print("Testing MCP Server HTTP POST Endpoints...")
    print("=" * 50)
    
    results = []
    for url, name in endpoints:
        results.append(test_endpoint(url, name))
    
    print("=" * 50)
    if all(results):
        print("✓ All endpoints working successfully!")
    else:
        print("✗ Some endpoints failed")

if __name__ == "__main__":
    main()
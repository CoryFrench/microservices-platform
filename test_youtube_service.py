#!/usr/bin/env python3

import requests
import json
import os

# Configuration
BASE_URL = "http://localhost:14300"
TEST_VIDEO_ID = "RlZWbr-_ivY"  # Real YouTube video ID provided by user
TEST_THUMB_URL = f"https://i.ytimg.com/vi/{TEST_VIDEO_ID}/hqdefault.jpg"

def test_health_check():
    """Test the health endpoint"""
    print("🏥 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_transcript_only():
    """Test transcript download only"""
    print("\n📜 Testing Transcript Download...")
    try:
        data = {"video_id": TEST_VIDEO_ID}
        response = requests.post(
            f"{BASE_URL}/download_transcript",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            transcript = result.get('transcript', [])
            print(f"✅ Transcript received: {len(transcript)} entries")
            if transcript:
                print(f"First entry: {transcript[0]}")
        else:
            print(f"❌ Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Transcript test failed: {e}")
        return False

def test_summarize_no_email():
    """Test summarization without email"""
    print("\n🤖 Testing Summarization (No Email)...")
    try:
        data = {
            "video_id": TEST_VIDEO_ID,
            "thumb_url": TEST_THUMB_URL,
            "channel_name": "TestChannel",
            "send_email": False
        }
        response = requests.post(
            f"{BASE_URL}/summarize",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Summary generated for video: {result.get('video_id')}")
            print(f"Email sent: {result.get('email_sent')}")
            summary = result.get('summary', '')
            print(f"Summary preview: {summary[:200]}...")
        else:
            print(f"❌ Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Summarization test failed: {e}")
        return False

def test_zapier_like_call():
    """Test a call that mimics what Zapier would send"""
    print("\n🔗 Testing Zapier-like Call...")
    
    # This mimics the original lambda_handler input
    zapier_data = {
        "video_id": TEST_VIDEO_ID,
        "thumb_url": TEST_THUMB_URL,
        "channel_name": "HousingWire",
        "send_email": False  # Set to False for testing
    }
    
    print("Zapier-like payload:")
    print(json.dumps(zapier_data, indent=2))
    
    try:
        response = requests.post(
            f"{BASE_URL}/summarize",
            json=zapier_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"\nStatus: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Zapier-like call successful!")
            print(f"Video ID: {result.get('video_id')}")
            print(f"Email sent: {result.get('email_sent')}")
            print("Summary generated successfully ✅")
        else:
            print(f"❌ Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Zapier-like test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting YouTube Summary Service Tests")
    print("=" * 50)
    
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set")
        print("   The summarization tests will fail without it")
    
    tests = [
        ("Health Check", test_health_check),
        ("Transcript Download", test_transcript_only),
        ("Summarization (No Email)", test_summarize_no_email),
        ("Zapier-like Call", test_zapier_like_call)
    ]
    
    results = []
    for test_name, test_func in tests:
        success = test_func()
        results.append((test_name, success))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")

if __name__ == "__main__":
    main() 
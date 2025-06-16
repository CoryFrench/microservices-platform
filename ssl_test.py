#!/usr/bin/env python3
"""
SSL Certificate Test Script
Tests SSL certificate validity and connection to services.waterfront-ai.com
"""

import ssl
import socket
import datetime
import requests
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings for testing
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def test_ssl_certificate(hostname, port=443):
    """Test SSL certificate for a given hostname and port"""
    print(f"\n=== Testing SSL Certificate for {hostname}:{port} ===")
    
    try:
        # Create SSL context
        context = ssl.create_default_context()
        
        # Connect to the server
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Get certificate info
                cert = ssock.getpeercert()
                
                print(f"✅ SSL Connection successful!")
                print(f"Subject: {dict(x[0] for x in cert['subject'])}")
                print(f"Issuer: {dict(x[0] for x in cert['issuer'])}")
                print(f"Version: {cert['version']}")
                print(f"Serial Number: {cert['serialNumber']}")
                
                # Check expiration
                not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_until_expiry = (not_after - datetime.datetime.now()).days
                print(f"Expires: {cert['notAfter']} ({days_until_expiry} days from now)")
                
                # Check Subject Alternative Names
                if 'subjectAltName' in cert:
                    san_list = [name[1] for name in cert['subjectAltName']]
                    print(f"Subject Alternative Names: {', '.join(san_list)}")
                
                return True
                
    except ssl.SSLError as e:
        print(f"❌ SSL Error: {e}")
        return False
    except socket.timeout:
        print(f"❌ Connection timeout")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_http_endpoints(base_url):
    """Test HTTP endpoints"""
    print(f"\n=== Testing HTTP Endpoints for {base_url} ===")
    
    endpoints = [
        "/health",
        "/api/send-email/health",
        "/api/chatgpt-daily/health",
        "/api/calendar-backend/health"
    ]
    
    headers = {
        'X-API-Key': '6ec14ed9-7485-492a-9393-b3df17967945',
        'User-Agent': 'SSL-Test-Script/1.0'
    }
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            status = "✅" if response.status_code == 200 else "⚠️"
            print(f"{status} {endpoint}: {response.status_code} - {response.text[:50]}...")
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint}: Error - {str(e)[:50]}...")

def main():
    """Main test function"""
    hostname = "services.waterfront-ai.com"
    
    print("🔒 SSL Certificate and Connection Test")
    print("=" * 50)
    
    # Test SSL certificate
    ssl_ok = test_ssl_certificate(hostname)
    
    # Test HTTPS endpoints
    if ssl_ok:
        test_http_endpoints(f"https://{hostname}")
    else:
        print("\n⚠️ SSL test failed, trying HTTP endpoints...")
        test_http_endpoints(f"http://{hostname}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    main() 
import requests
import json

def test_server():
    """Test the email server endpoint"""
    
    # Test data
    test_data = {
        "subject": "Test Email Subject",
        "message_text": "This is a test email message with custom content."
    }
    
    try:
        # Test health check
        health_response = requests.get("http://localhost:5000/")
        print("Health Check:", health_response.json())
        
        # Test OpenAPI spec
        spec_response = requests.get("http://localhost:5000/openapi.json")
        print("OpenAPI Spec Available:", spec_response.status_code == 200)
        
        # Test email sending (uncomment when ready to test)
        # email_response = requests.post(
        #     "http://localhost:5000/send-email",
        #     json=test_data,
        #     headers={"Content-Type": "application/json"}
        # )
        # print("Email Response:", email_response.json())
        
        print("Server is working correctly!")
        
    except requests.exceptions.ConnectionError:
        print("Server is not running. Start it with: python server.py")
    except Exception as e:
        print(f"Error testing server: {e}")

if __name__ == "__main__":
    test_server() 
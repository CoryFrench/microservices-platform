from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from send_email import send_email
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for ChatGPT Custom GPTs

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Email service is running"})

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Docker healthcheck"""
    return jsonify({"status": "healthy", "message": "Email service is running"})

@app.route('/send-email', methods=['POST'])
def send_email_endpoint():
    """
    Send email endpoint for ChatGPT Custom GPTs
    
    Expected JSON payload:
    {
        "subject": "Email subject line",
        "message_text": "Email body text"
    }
    
    Note: All emails are sent to cory@wfpcc.com from customgpt@wfpcc.com
    """
    try:
        # Get API key from environment
        api_key = os.getenv('MAILCHIMP_API_KEY')
        if not api_key:
            return jsonify({
                "success": False,
                "error": "API key not found in environment variables"
            }), 500

        # Parse request data
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['subject', 'message_text']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                "success": False,
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        # Extract data
        subject = data['subject']
        message_text = data['message_text']
        from_email = "customgpt@wfpcc.com"  # Hardcoded for consistency
        to_email = "cory@wfpcc.com"  # Hardcoded for security

        # Send email using the existing function
        result = send_email(
            api_key=api_key,
            subject=subject,
            message_text=message_text,
            from_email=from_email,
            to_email=to_email
        )

        # Check if email was sent successfully
        if isinstance(result, list) and len(result) > 0:
            email_result = result[0]
            if email_result.get('status') == 'sent':
                return jsonify({
                    "success": True,
                    "message": "Email sent successfully",
                    "result": result
                })
            else:
                return jsonify({
                    "success": False,
                    "error": f"Email failed to send: {email_result.get('reject_reason', 'Unknown error')}",
                    "result": result
                }), 400
        else:
            return jsonify({
                "success": False,
                "error": "Unexpected response from email service",
                "result": result
            }), 500

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/openapi.json', methods=['GET'])
def openapi_spec():
    """OpenAPI specification for ChatGPT Custom GPTs"""
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Email Service API",
            "description": "API for sending emails with video summaries",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": "http://localhost:5000",
                "description": "Local development server"
            }
        ],
        "paths": {
            "/send-email": {
                "post": {
                    "summary": "Send a custom email",
                    "description": "Sends an email with custom subject and message text",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["subject", "message_text"],
                                    "properties": {
                                        "subject": {
                                            "type": "string",
                                            "description": "The email subject line"
                                        },
                                        "message_text": {
                                            "type": "string",
                                            "description": "The email body text content"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Email sent successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {"type": "boolean"},
                                            "message": {"type": "string"},
                                            "result": {"type": "object"}
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Bad request - missing fields or email failed",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {"type": "boolean"},
                                            "error": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        },
                        "500": {
                            "description": "Internal server error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {"type": "boolean"},
                                            "error": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return jsonify(spec)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 14500))
    app.run(debug=True, host='0.0.0.0', port=port) 
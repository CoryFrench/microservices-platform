#!/bin/bash

# SSL Certificate Renewal Script for services.waterfront-ai.com
# This script renews Let's Encrypt certificates and reloads nginx

echo "Starting SSL certificate renewal process..."

# Navigate to the project directory
cd /c/Users/WaterfrontAI/Documents/Repos/microservices-platform

# Renew certificates using certbot
echo "Renewing certificates..."
docker-compose run --rm certbot renew

# Check if renewal was successful
if [ $? -eq 0 ]; then
    echo "Certificate renewal successful!"
    
    # Reload nginx to pick up new certificates
    echo "Reloading nginx..."
    docker-compose exec reverse-proxy nginx -s reload
    
    if [ $? -eq 0 ]; then
        echo "Nginx reloaded successfully!"
        echo "SSL certificate renewal completed successfully."
    else
        echo "Error: Failed to reload nginx"
        exit 1
    fi
else
    echo "Error: Certificate renewal failed"
    exit 1
fi

echo "SSL renewal process completed." 
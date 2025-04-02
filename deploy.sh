#!/bin/bash

# Script to deploy the frontend to S3
# Run this from your Cloud9 environment after CI completes on GitHub

echo "Starting deployment process..."

# Navigate to the project directory
cd ~/environment/ai-diet-planner

# Pull the latest code from GitHub
echo "Pulling latest code from GitHub..."
git pull origin main

# Build the frontend
echo "Building frontend..."
cd frontend
npm ci
npm run build

# Deploy to S3
echo "Deploying to S3..."
aws s3 sync build/ s3://ai-diet-planner-x23293519 --delete

echo "Deployment completed successfully!"
echo "Visit your website at: http://ai-diet-planner-x23293519.s3-website-eu-west-1.amazonaws.com"
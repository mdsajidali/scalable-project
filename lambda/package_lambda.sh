#!/bin/bash

# Create a deployment package for our Lambda function
mkdir -p package
cd meal_planner
zip -r ../package/lambda_function.zip lambda_function.py
cd ..

echo "Lambda package created at package/lambda_function.zip"
echo "You can now upload this ZIP file to AWS Lambda via the AWS console"
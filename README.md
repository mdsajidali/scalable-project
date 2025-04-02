# scalable-project
# AI Diet Planner - Installation Guide

This document provides step-by-step instructions for setting up and running the AI Diet Planner application.

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- NPM 8 or higher
- AWS Account with access to:
  - Elastic Beanstalk
  - Lambda
  - S3
  - IAM

## Project Structure

The project is divided into two main components:

- `backend/`: Django REST API
- `frontend/`: React application
- `lambda/`: AWS Lambda function for meal planning

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/mdsajidali/scalable-project.git
cd scalable-project
```

### 2. Set Up Backend

#### Create a Python Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Set Up Environment Variables

Create a `.env` file in the backend directory with the following variables:

```
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
WEATHER_API_KEY=your_weather_api_key
FITNESS_API_URL=https://l734p4kw4i.execute-api.eu-west-1.amazonaws.com/Prod
AWS_REGION=eu-west-1
AWS_LAMBDA_FUNCTION_NAME=x23293519_fitness_meal
```

#### Initialize Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

#### Run Development Server

```bash
python manage.py runserver
```

### 3. Set Up Frontend

```bash
cd ../frontend
npm install
```

#### Set Up Environment Variables

Create a `.env` file in the frontend directory:

```
REACT_APP_API_URL=http://localhost:8000
```

#### Run Development Server

```bash
npm start
```

## Deployment Instructions

### Backend Deployment to AWS Elastic Beanstalk

1. Install the EB CLI:
   ```bash
   pip install awsebcli
   ```

2. Initialize Elastic Beanstalk:
   ```bash
   cd backend
   eb init -p python-3.9 ai-diet-planner --region eu-west-1
   ```

3. Create an environment:
   ```bash
   eb create diet-planner
   ```

4. Set environment variables:
   ```bash
   eb setenv DJANGO_SECRET_KEY=your_secret_key DJANGO_DEBUG=False WEATHER_API_KEY=your_weather_api_key FITNESS_API_URL=https://l734p4kw4i.execute-api.eu-west-1.amazonaws.com/Prod AWS_REGION=eu-west-1 AWS_LAMBDA_FUNCTION_NAME=x23293519_fitness_meal
   ```

5. Deploy:
   ```bash
   eb deploy
   ```

### Frontend Deployment to AWS S3

1. Build the React app:
   ```bash
   cd frontend
   REACT_APP_API_URL=http://your-backend-url.elasticbeanstalk.com npm run build
   ```

2. Create an S3 bucket and configure it for static website hosting.

3. Upload the build folder contents to the S3 bucket:
   ```bash
   aws s3 sync build/ s3://your-bucket-name --delete
   ```

### Lambda Function Deployment

1. Create a Lambda function in AWS Console:
   - Runtime: Python 3.9
   - Function name: x23293519_fitness_meal

2. Package the Lambda function:
   ```bash
   cd lambda
   zip -r ../lambda_function.zip meal_planner/
   ```

3. Upload the ZIP file to your Lambda function.

4. Configure IAM permissions to allow Elastic Beanstalk to invoke Lambda:
   - Go to IAM console
   - Find the role used by your Elastic Beanstalk EC2 instances
   - Add an inline policy:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": "lambda:InvokeFunction",
               "Resource": "arn:aws:lambda:eu-west-1:your-account-id:function:x23293519_fitness_meal"
           }
       ]
   }
   ```

## Using the Application

1. Register a new user account
2. Set up your profile with physical information and dietary preferences
3. Generate meal plans based on your location and fitness data

## Troubleshooting

- If meal plans show default values, check that:
  - The Lambda function has been deployed correctly
  - Elastic Beanstalk has permission to invoke the Lambda function
  - A fitness API ID has been set in your user profile

- If the frontend cannot connect to the backend:
  - Ensure CORS is properly configured in the backend
  - Verify the API URL is correct in the frontend environment

## Contact Information

For support or questions, please contact:
Mohd Sajid Ali - X23293519@student.ncirl.ie
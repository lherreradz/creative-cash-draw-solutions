#!/bin/bash

# Deployment script for AWS Lambda container
# Creative Cash Draw Solutions - Change Calculator

set -e

# Configuration - Update these variables
IMAGE_NAME="change-calculator"
TAG="latest"
FUNCTION_NAME="change-calculator-container"
AWS_REGION="${AWS_REGION:-us-east-1}"
AWS_ACCOUNT_ID="${AWS_ACCOUNT_ID}"
MEMORY_SIZE=512
TIMEOUT=30

# ECR Repository URI
ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:${TAG}"

echo "Deploying AWS Lambda container for Change Calculator..."
echo "Function Name: ${FUNCTION_NAME}"
echo "Image URI: ${ECR_URI}"
echo "Region: ${AWS_REGION}"

# Check if function exists
if aws lambda get-function --function-name ${FUNCTION_NAME} --region ${AWS_REGION} >/dev/null 2>&1; then
    echo "Updating existing Lambda function..."
    aws lambda update-function-code \
        --function-name ${FUNCTION_NAME} \
        --image-uri ${ECR_URI} \
        --region ${AWS_REGION}
else
    echo "Creating new Lambda function..."
    aws lambda create-function \
        --function-name ${FUNCTION_NAME} \
        --package-type Image \
        --code ImageUri=${ECR_URI} \
        --architectures x86_64 \
        --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/lambda-execution-role \
        --memory-size ${MEMORY_SIZE} \
        --timeout ${TIMEOUT} \
        --region ${AWS_REGION}
fi

echo "✅ Lambda function deployed successfully!"
echo ""
echo "Function ARN:"
aws lambda get-function --function-name ${FUNCTION_NAME} --region ${AWS_REGION} --query 'Configuration.FunctionArn' --output text
echo ""
echo "Next steps:"
echo "1. Create API Gateway (if not already done)"
echo "2. Configure CORS and permissions"
echo "3. Test the API endpoints"
echo ""
echo "To create API Gateway:"
echo "aws apigateway create-rest-api --name 'ChangeCalculatorAPI' --region ${AWS_REGION}"
#!/bin/bash

# Build script for AWS Lambda container image
# Creative Cash Draw Solutions - Change Calculator

set -e

# Configuration
IMAGE_NAME="change-calculator"
TAG="latest"
ECR_REPOSITORY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}"

echo "Building AWS Lambda container image for Change Calculator..."
echo "Image name: ${IMAGE_NAME}:${TAG}"

# Build the Docker image
echo "Building Docker image..."
docker build -t ${IMAGE_NAME}:${TAG} .

# Tag for ECR
echo "Tagging image for ECR..."
docker tag ${IMAGE_NAME}:${TAG} ${ECR_REPOSITORY}:${TAG}

# Authenticate Docker with ECR
echo "Authenticating with AWS ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Create ECR repository if it doesn't exist
echo "Ensuring ECR repository exists..."
aws ecr describe-repositories --repository-names ${IMAGE_NAME} --region ${AWS_REGION} || \
aws ecr create-repository --repository-name ${IMAGE_NAME} --region ${AWS_REGION}

# Push to ECR
echo "Pushing image to ECR..."
docker push ${ECR_REPOSITORY}:${TAG}

echo "✅ Container image built and pushed successfully!"
echo "ECR Image URI: ${ECR_REPOSITORY}:${TAG}"
echo ""
echo "Next steps:"
echo "1. Create/update Lambda function with container image"
echo "2. Configure API Gateway"
echo "3. Test the deployment"
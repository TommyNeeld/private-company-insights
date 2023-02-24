#!/bin/bash -e

echo "current working directory: $(pwd)"
. ./src/version.env

echo "App version is $VERSION"

account_id=$(aws sts get-caller-identity --query Account --output text)
registry=$account_id.dkr.ecr.eu-west-1.amazonaws.com
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin $registry

image=specter-dash-app
echo
echo "Building and pushing image for $image..."
aws ecr create-repository --repository-name $image || true
docker buildx build --platform linux/amd64 --push -t $registry/$image:$VERSION .
echo "pushed to $registry/$image:$VERSION -> ensure terraform sees that"

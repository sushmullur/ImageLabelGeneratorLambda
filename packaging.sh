#!/bin/bash

# Define the build directory and the handler script
BUILD_DIR="./build"
HANDLER_SCRIPT="index.py"

rm -rf $BUILD_DIR

# Ensure the build directory exists
mkdir $BUILD_DIR

# Copy the handler script to the build directory
cp $HANDLER_SCRIPT $BUILD_DIR/

# Use the lambci Docker image that matches Lambda's environment
docker run --rm -v "$PWD":/var/task "lambci/lambda:build-python3.8" bash -c "
    yum install -y gcc-c++ && \
    cd /var/task/build && \
    pip3 install numpy boto3 aws-lambda-powertools opencv-python-headless --target=./"

# Navigate to the build directory
cd $BUILD_DIR

# Zip the contents for Lambda deployment
zip -r9 ImageProcessor.zip .

# Move the zip file to the project directory
mv ImageProcessor.zip ..

# Move back to the project directory
cd ..

# Optional: Cleanup by removing build directory
rm -rf $BUILD_DIR

mkdir build
mv ImageProcessor.zip build/

# Echo completion
echo "Lambda function package is ready: ImageProcessor.zip"

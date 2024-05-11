#!/bin/bash

# Define the build directory and the script directory
BUILD_DIR="./build"
SRC_DIR="./src"

# Clean existing build directory
rm -rf $BUILD_DIR

# Ensure the build directory exists
mkdir -p $BUILD_DIR

# Copy all source files to the build directory
cp -R $SRC_DIR/* $BUILD_DIR/

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

# Cleanup by removing build directory
cd ..
rm -rf $BUILD_DIR

# Prepare the build directory for the zip file
mkdir -p build
mv ImageProcessor.zip build/

# Echo completion
echo "Lambda function package is ready: ImageProcessor.zip"

#!/bin/bash

# Print commands and their arguments as they are executed
set -x

# Exit immediately if a command exits with a non-zero status
set -e

# Ensure we're in the project directory
cd /vercel/path0

# Install pip if not available
if ! command -v pip &> /dev/null
then
    echo "pip could not be found, installing pip"
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
fi

# Install requirements
pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput

# Ensure the static files are moved to the correct directory
mkdir -p staticfiles_build
cp -r static/* staticfiles_build/

#!/bin/bash

#  Script to set up a Jenkins agent for running Playwright tests

# Install required packages
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    wget \
    git \
    zip \
    unzip \
    nodejs \
    npm \
    openjdk-11-jdk

# Create Python symlinks
sudo ln -sf /usr/bin/python3 /usr/bin/python
sudo ln -sf /usr/bin/pip3 /usr/bin/pip

# Create a virtual environment
python -m venv ~/venv
source ~/venv/bin/activate

# Install Python packages
pip install pytest pytest-xdist pytest-html playwright python-dotenv allure-pytest

# Install Playwright browsers
python -m playwright install
python -m playwright install-deps

# Install Allure command-line tool
curl -o allure-2.22.0.tgz -Ls https://github.com/allure-framework/allure2/releases/download/2.22.0/allure-2.22.0.tgz
sudo tar -zxvf allure-2.22.0.tgz -C /opt/
sudo ln -s /opt/allure-2.22.0/bin/allure /usr/local/bin/allure
rm allure-2.22.0.tgz

echo "Jenkins agent setup complete. Ready to run Playwright tests."
 
#  Jenkins CI Setup Guide

This document explains how to set up and configure Jenkins for running the test automation framework.

## Prerequisites

1. Jenkins server installed
2. Python 3.10+ installed on Jenkins agent
3. Allure command-line tools installed (for report generation)

## Jenkins Configuration

### Required Plugins

Install the following Jenkins plugins:
- Pipeline
- AnsiColor
- Allure Jenkins Plugin
- JUnit Plugin
- Timestamper
- Workspace Cleanup

### Global Tool Configuration

1. Go to "Manage Jenkins" > "Global Tool Configuration"
2. Configure Python installation (if not using system Python)
3. Configure Allure command-line installation

### Creating the Jenkins Pipeline

1. Create a new Pipeline job
2. Choose "Pipeline script from SCM" as the definition
3. Set up your SCM (Git, etc.) with repository URL and credentials
4. Specify the path to the Jenkinsfile (default: "Jenkinsfile" in the root)
5. Save the configuration

## Pipeline Parameters

The Jenkinsfile defines several parameters that you can customize for each build:

- **BROWSER**: Browser to use for tests (chromium, firefox, webkit)
- **TEST_GROUP**: Test group to run (all, smoke, search, cart, checkout)
- **HEADLESS**: Whether to run tests in headless mode
- **PARALLEL**: Whether to run tests in parallel
- **WORKERS**: Number of parallel workers when running in parallel
- **ENVIRONMENT**: Environment to run tests against (staging, dev, prod)
- **GENERATE_ALLURE**: Whether to generate Allure reports
- **GENERATE_HTML**: Whether to generate HTML reports

## Scheduled Runs

The pipeline is configured to run daily at midnight using the cron trigger (`0 0 * * *`).
You can modify this schedule in the Jenkinsfile.

## Notifications

The pipeline is configured to send email notifications when tests fail.
Update the email address in the Jenkinsfile's `post.failure` section.

## Viewing Test Results

1. Allure Reports: Available through the Allure plugin in the build results
2. JUnit Reports: Available through the JUnit plugin in the build results
3. Artifacts: Screenshots, videos, and logs are archived for each build
 
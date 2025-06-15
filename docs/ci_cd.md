#  CI/CD Integration with Jenkins

This framework is designed to integrate seamlessly with Jenkins CI/CD pipelines. The repository includes configuration files for setting up Jenkins pipelines to run the test automation framework.

## Jenkins Pipeline Configuration

The main Jenkinsfile defines a pipeline with the following features:

- Parameterized builds for flexibility
- Daily scheduled runs
- Cross-browser testing
- Parallel test execution
- Environment-specific configuration
- Allure and HTML report generation
- Artifact archiving (screenshots, videos, logs)
- Email notifications on test failures

```groovy
pipeline {
    agent any
    
    parameters {
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Browser to run tests with')
        choice(name: 'TEST_GROUP', choices: ['all', 'smoke', 'search', 'cart', 'checkout'], description: 'Test group to run')
        booleanParam(name: 'HEADLESS', defaultValue: true, description: 'Run in headless mode')
        booleanParam(name: 'PARALLEL', defaultValue: true, description: 'Run tests in parallel')
        string(name: 'WORKERS', defaultValue: '4', description: 'Number of parallel workers')
        choice(name: 'ENVIRONMENT', choices: ['staging', 'dev', 'prod'], defaultValue: 'staging', description: 'Environment to run tests against')
        booleanParam(name: 'GENERATE_ALLURE', defaultValue: true, description: 'Generate Allure reports')
        booleanParam(name: 'GENERATE_HTML', defaultValue: true, description: 'Generate HTML reports')
    }
    
    // Pipeline stages...
}
```

## Jenkins Setup Options

The repository provides multiple options for setting up Jenkins:

1. **Basic Pipeline**: Use the `Jenkinsfile` in the root directory for a simple pipeline setup.
2. **Multibranch Pipeline**: Use `jenkins/Jenkinsfile.multibranch` for testing multiple branches with branch-specific configurations.
3. **Job DSL**: Use `jenkins/job_dsl.groovy` to programmatically create multiple test jobs with different configurations.

## Setting Up the Jenkins Pipeline

1. Install required Jenkins plugins:
   - Pipeline
   - Allure Jenkins Plugin
   - JUnit Plugin
   - AnsiColor
   - Timestamper
   - Workspace Cleanup

2. Create a new Pipeline job:
   - Go to Jenkins dashboard and click "New Item"
   - Enter a name for the job and select "Pipeline"
   - In the job configuration, under "Pipeline", select "Pipeline script from SCM"
   - Select "Git" as the SCM
   - Enter your repository URL and credentials
   - Specify the branch to build (e.g., `main`)
   - Set the script path to `Jenkinsfile`
   - Save the configuration

3. Run the pipeline:
   - Go to the job page and click "Build with Parameters"
   - Configure the parameters as needed
   - Click "Build"

## Viewing Test Reports

After the pipeline runs:

1. Allure Reports:
   - Click on the build number
   - Click on "Allure Report" in the left sidebar

2. JUnit Reports:
   - Click on the build number
   - Click on "Test Result" in the left sidebar

3. Artifacts:
   - Click on the build number
   - Click on "Artifacts" in the left sidebar
   - Download screenshots, videos, or logs as needed

## Best Practices for Jenkins CI Integration

1. **Run smoke tests first**: Configure your pipeline to run smoke tests before more extensive test suites to catch major issues early.
2. **Use multiple agents**: If available, distribute test execution across multiple Jenkins agents for faster feedback.
3. **Use environment-specific configuration**: Set environment variables to configure the tests for different environments.
4. **Implement retries for flaky tests**: Use the `--reruns` flag with pytest to retry failed tests a few times before marking them as failures.
5. **Configure notifications**: Set up email or Slack notifications to alert the team when tests fail.
6. **Archive test artifacts**: Make sure screenshots, videos, logs, and reports are captured and archived for debugging failed tests.
7. **Use consistent naming**: Use consistent naming conventions for jobs and parameters to maintain clarity.

## Advanced Jenkins Features

### Parallel Test Execution

For large test suites, consider using the Jenkins `parallel` step to run different test groups simultaneously:

```groovy
stage('Run Tests') {
    parallel {
        stage('Smoke Tests') {
            steps {
                sh 'python run_tests.py --browser chromium --headless --markers smoke'
            }
        }
        stage('Cart Tests') {
            steps {
                sh 'python run_tests.py --browser chromium --headless --markers cart'
            }
        }
        stage('Checkout Tests') {
            steps {
                sh 'python run_tests.py --browser chromium --headless --markers checkout'
            }
        }
    }
}
```

### Matrix Builds

For cross-browser testing, you can use matrix builds with Jenkins:

```groovy
matrix {
    axes {
        axis {
            name 'BROWSER'
            values 'chromium', 'firefox', 'webkit'
        }
        axis {
            name 'TEST_GROUP'
            values 'smoke', 'search', 'cart', 'checkout'
        }
    }
    stages {
        stage('Run Tests') {
            steps {
                sh "python run_tests.py --browser ${BROWSER} --headless --markers ${TEST_GROUP}"
            }
        }
    }
}
```
 
pipeline  {
    agent {
        dockerfile {
            filename 'jenkins/Dockerfile.agent'
            args '--shm-size=1g'
        }
    }
    
    parameters {
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Browser to run tests on')
        choice(name: 'ENVIRONMENT', choices: ['staging', 'prod'], description: 'Environment to run tests against')
        booleanParam(name: 'HEADLESS', defaultValue: true, description: 'Run in headless mode')
        booleanParam(name: 'GENERATE_REPORT', defaultValue: true, description: 'Generate Allure report')
        string(name: 'TEST_MARKERS', defaultValue: '', description: 'Run tests with specific markers (comma-separated, leave empty for all tests)')
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'mkdir -p reports screenshots videos traces allure-results'
                sh 'python -m pip install -r requirements.txt'
                sh 'playwright install'
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    def testCommand = "python run_tests.py --browser ${params.BROWSER} --env ${params.ENVIRONMENT}"
                    
                    if (!params.HEADLESS) {
                        testCommand += " --headed"
                    }
                    
                    if (params.GENERATE_REPORT) {
                        testCommand += " --allure"
                    }
                    
                    if (params.TEST_MARKERS) {
                        testCommand += " --marker \"${params.TEST_MARKERS}\""
                    }
                    
                    sh testCommand
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'screenshots/*, videos/*, traces/*, reports/*', allowEmptyArchive: true
            
            script {
                if (params.GENERATE_REPORT) {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'allure-results']]
                    ])
                }
            }
        }
        
        success {
            echo 'All tests passed!'
        }
        
        failure {
            echo 'Tests failed! Check screenshots, videos, and reports for details.'
        }
    }
}
 
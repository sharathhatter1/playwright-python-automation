//  Job DSL script to automatically create Jenkins pipeline jobs

folder('TestAutomation') {
    description('Test Automation Framework Jobs')
}

pipelineJob('TestAutomation/MainTestPipeline') {
    description('Runs the test automation suite')
    
    parameters {
        choiceParam('BROWSER', ['chromium', 'firefox', 'webkit'], 'Browser to use for testing')
        choiceParam('TEST_GROUP', ['all', 'smoke', 'search', 'cart', 'checkout'], 'Test group to run')
        booleanParam('HEADLESS', true, 'Run in headless mode')
        booleanParam('PARALLEL', true, 'Run tests in parallel')
        stringParam('WORKERS', '4', 'Number of parallel workers')
        choiceParam('ENVIRONMENT', ['staging', 'dev', 'prod'], 'Environment to run tests against')
        booleanParam('GENERATE_ALLURE', true, 'Generate Allure reports')
        booleanParam('GENERATE_HTML', true, 'Generate HTML reports')
    }
    
    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url('YOUR_REPOSITORY_URL')
                        credentials('YOUR_CREDENTIALS_ID')
                    }
                    branch('main')
                }
            }
            scriptPath('Jenkinsfile')
        }
    }
    
    triggers {
        cron('0 0 * * *')
    }
    
    properties {
        disableConcurrentBuilds()
        buildDiscarder {
            strategy {
                logRotator {
                    daysToKeepStr('30')
                    numToKeepStr('20')
                    artifactDaysToKeepStr('7')
                    artifactNumToKeepStr('5')
                }
            }
        }
    }
}

// Create jobs for different browser/test group combinations
def browsers = ['chromium', 'firefox', 'webkit']
def testGroups = ['smoke', 'search', 'cart', 'checkout']

browsers.each { browser ->
    testGroups.each { testGroup ->
        pipelineJob("TestAutomation/${browser}-${testGroup}") {
            description("Runs ${testGroup} tests on ${browser}")
            
            definition {
                cps {
                    script('''
                        pipeline {
                            agent any
                            
                            stages {
                                stage('Run Tests') {
                                    steps {
                                        sh 'python run_tests.py --browser ''' + browser + ''' --headless --markers ''' + testGroup + ''' --parallel --allure'
                                    }
                                }
                            }
                            
                            post {
                                always {
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
                    '''.stripIndent())
                    sandbox()
                }
            }
            
            triggers {
                cron('0 3 * * *')
            }
        }
    }
}

// Create a multibranch pipeline job
multibranchPipelineJob('TestAutomation/MultiBranchTests') {
    description('Runs tests on multiple branches')
    
    branchSources {
        git {
            id('1')
            remote('YOUR_REPOSITORY_URL')
            credentialsId('YOUR_CREDENTIALS_ID')
            includes('main develop feature/*')
        }
    }
    
    orphanedItemStrategy {
        discardOldItems {
            numToKeep(20)
            daysToKeep(30)
        }
    }
    
    triggers {
        periodic(1440) // Check for new branches/commits every 24 hours
    }
    
    factory {
        workflowBranchProjectFactory {
            scriptPath('jenkins/Jenkinsfile.multibranch')
        }
    }
}
 
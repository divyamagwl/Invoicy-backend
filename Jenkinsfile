pipeline {
    agent any

    environment
    {
        registry = "divyamagwl/invoicy-backend"
        registryCredential = "dockerhub"
        dockerImage = ""
    }

    stages {
        stage('Pull GitHub') {
            steps {
                git branch: 'main', url: 'https://github.com/divyamagwl/Invoicy-backend'
            }
        }

        def installed = fileExists 'bin/activate'
        if (!installed) {
            stage("Install Python Virtual Enviroment") {
                sh 'virtualenv --no-site-packages .'
            }
        }           
        stage ("Install Application Dependencies") {
            sh '''
                source bin/activate
                pip install -r backend/requirements.txt
                deactivate
            '''
        }
        stage ("Run Unit/Integration Tests") {
            def testsError = null
            try {
                sh '''
                    source ../bin/activate
                    python3 backend/manage.py test
                    deactivate
                '''
            }
            catch(err) {
                testsError = err
                currentBuild.result = 'FAILURE'
            }
            finally {
                if (testsError) {
                    throw testsError
                }
            }
        }

        stage('Docker Image Build') {
            steps {
                dir("backend/") {
                    script {
                        dockerImage = docker.build(registry + ":latest")
                    }
                }
            }
        }
        stage('DockerHub Image Push') {
            steps {
                script {
                    docker.withRegistry('', registryCredential) {
                        dockerImage.push()
                    }
                }
            }
        }
        stage('Ansible Deployment') {
            steps {
                ansiblePlaybook colorized: true,
                installation: 'Ansible',
                inventory: 'inventory',
                playbook: 'playbook.yml'
            }
        }
    }
}
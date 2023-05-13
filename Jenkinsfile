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

        stage("Install Python Virtual Enviroment") {
            steps {
                sh 'virtualenv --no-site-packages .'
            }
        }           
        stage ("Install Application Dependencies") {
            steps {
                sh '''
                    source bin/activate
                    pip install -r backend/requirements.txt
                    deactivate
                '''
            }
        }
        stage ("Run Unit/Integration Tests") {
            steps {
                sh '''
                    source ../bin/activate
                    python3 backend/manage.py test
                    deactivate
                '''
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
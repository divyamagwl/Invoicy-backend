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

        stage('Setup Python Virtual Environment'){
            steps {
                sh '''
                    chmod +x envsetup.sh
                    ./envsetup.sh
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
pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/ShivkumarChougala/Basic-Randsomware'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Build') {
            steps {
                echo 'Build step (can be extended later)'
            }
        }

        stage('Test') {
            steps {
                echo 'Running watcher.py to monitor files...'
                sh 'python3 watcher.py'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploy step (can be customized)'
            }
        }
    }
}


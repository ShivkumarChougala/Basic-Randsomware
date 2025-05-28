pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = 1
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/ShivkumarChougala/Basic-Randsomware'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                sh 'pip3 install -r requirements.txt || true'
            }
        }

        stage('Build') {
            steps {
                echo 'Preparing for execution...'
            }
        }

        stage('Test') {
            steps {
                echo 'Running watcher.py to monitor files...'
                sh 'python3 watcher.py || echo "watcher.py failed, check logs"'
            }
        }

        stage('Deploy') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo 'Deployment stage (placeholder)'
            }
        }
    }

    post {
        success {
            echo '✅ Build completed successfully.'
        }
        failure {
            echo '❌ Build failed. Please check console output.'
        }
    }
}


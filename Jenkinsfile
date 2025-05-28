pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                // Use python3 and pip3
                sh 'python3 --version || true'    // Check python3 exists
                sh 'pip3 --version || true'       // Check pip3 exists
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run Watcher') {
            steps {
                echo 'Running watcher.py script...'
                sh 'python3 watcher.py'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deployment step - add your commands here'
                // Avoid shell commands with special chars here if not sure
            }
        }
    }

    post {
        failure {
            echo 'Build failed. Check console output for errors.'
        }
        success {
            echo 'Build completed successfully.'
        }
    }
}


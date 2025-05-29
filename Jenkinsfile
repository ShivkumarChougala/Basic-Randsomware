pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
              }
        }

        stage('Run Watcher') {
            steps {
                echo 'Running watcher.py script...'
               
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


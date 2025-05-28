pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'echo Compiling...'
                // Add your build commands here if needed
            }
        }
        stage('Test') {
            steps {
                sh 'echo Running watcher.py to monitor files...'
                sh 'python3 watcher.py'  // Run your watcher script
            }
        }
        stage('Deploy') {
            steps {
                sh 'echo Deploying (simulated)...'
            }
        }
    }
}


pipeline {
    agent any
    environment {
        DOCKER_HUB_USER = 'anwayalamwar'
        IMAGE_NAME      = 'welcome'
        IMAGE_TAG       = 'latest'
    }
    stages {
        stage('Build Image') {
            steps {
                sh "docker build -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials',
                                                 usernameVariable: 'DOCKER_USER',
                                                 passwordVariable: 'DOCKER_PASS')]) {
                    sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
                    sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }
        stage('Deploy to Swarm') {
            steps {
                // This single command safely creates the service if new, or updates it if it exists
                sh """
                docker service create --name welcome-service --publish 5000:5000 ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} || \
                docker service update --image ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} --force welcome-service
                """
            }
        }
    }
}


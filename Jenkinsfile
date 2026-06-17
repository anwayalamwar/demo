pipeline {
    agent any
    environment {
        DOCKER_HUB_USER = 'anwayalamwar'
        IMAGE_NAME      = 'welcome'
        IMAGE_TAG       = 'latest'
        CONTAINER_NAME  = 'welcome-container'
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
        stage('Deploy Container Locally') {
            steps {
                // 1. Stop and remove the old container if it exists
                sh "docker rm -f ${CONTAINER_NAME} || true"
                
                // 2. Run the new container on port 5000
                sh "docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }
}


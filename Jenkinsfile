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
                stage('Deploy as Swarm Service') {
            steps {
                script {
                    // Check if the service already exists
                    def serviceExists = sh(script: "docker service ls --filter name=welcome-service -q", returnStdout: true).trim()
                    
                    if (serviceExists) {
                        // 1. If it exists, update it with the fresh image
                        sh "docker service update --image ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} --force welcome-service"
                    } else {
                        // 2. If it is new, create the service on port 5000
                        sh "docker service create --name welcome-service --publish 5000:5000 ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }



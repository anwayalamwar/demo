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
                sh """
                # 1. Smart Check: Only initialize if not already in a swarm
                if ! docker info | grep -q "Swarm: active"; then
                    docker swarm init
                fi

                # 2. Deploy or update using host mode to prevent routing mesh locks
                docker service create --name welcome-service --publish mode=host,published=5000,target=5000 ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} || \
                docker service update --image ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} --force welcome-service
                """
            }
        }
    }
}


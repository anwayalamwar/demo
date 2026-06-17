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
                # 1. Smart Check: Initialize swarm if it is off
                if ! docker info | grep -q "Swarm: active"; then
                    docker swarm init
                fi

                # 2. Cleanup: Remove the old service configuration
                docker service rm welcome-service || true

                # 3. Fresh Deploy with Resource Limits
                docker service create \
                  --name welcome-service \
                  --publish mode=host,published=5000,target=5000 \
                  --limit-cpu 0.5 \
                  --limit-memory 256m \
                  ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }
    }
    
    post {
        success {
            echo "SUCCESS: The pipeline completed perfectly and the Swarm service is live!"
        }
        failure {
            echo "FAILURE: The pipeline failed. Check the stage logs above."
        }
    }
}


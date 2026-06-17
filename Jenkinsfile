pipeline {
    agent any
    environment {
        DOCKER_HUB_USER = 'anwayalamwar'
        IMAGE_NAME      = 'welcome'
        IMAGE_TAG       = 'latest'
    }
    stages {
        stage('SonarQube Code Scan') {
            steps {
                withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
                    sh """
                    docker run --rm \
                      --add-host=host.docker.internal:host-gateway \
                      -v "\$(pwd):/usr/src" \
                      sonarsource/sonar-scanner-cli \
                      -Dsonar.projectKey=flask-welcome-app \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=http://docker.internal \
                      -Dsonar.token=\$SONAR_TOKEN
                    """
                }
            }
        }
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
                if ! docker info | grep -q "Swarm: active"; then
                    docker swarm init
                fi

                docker service rm welcome-service || true

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
            echo "SUCCESS: Code scanned, image pushed, and Swarm service is live!"
        }
        failure {
            echo "FAILURE: The pipeline failed. Check the stage logs above."
        }
    }
}


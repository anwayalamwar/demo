pipeline {
    agent any
    environment {
        DOCKER_HUB_USER = 'anwayalamwar'
        IMAGE_NAME      = 'welcome'
        IMAGE_TAG       = 'latest'
        // 🔴 CHANGE THIS to your real email address
        NOTIFY_EMAIL    = 'arohitsharma2000@gmail.com' 
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

                # 3. Fresh Deploy with Resource Limits:
                # --limit-cpu 0.5 restricts the app to half a CPU core max
                # --limit-memory 256m restricts the app to 256 Megabytes of RAM max
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
    
    // 🔔 Automation Alerts Section
    post {
        success {
            echo "Pipeline succeeded! Sending alert..."
            mail to: "${NOTIFY_EMAIL}",
                 subject: "SUCCESS: Jenkins Build #${BUILD_NUMBER} - ${JOB_NAME}",
                 body: "Great news! The pipeline completed successfully. Your Flask app is running on Docker Swarm. Check it here: ${BUILD_URL}"
        }
        failure {
            echo "Pipeline failed! Sending alert..."
            mail to: "${NOTIFY_EMAIL}",
                 subject: "FAILURE: Jenkins Build #${BUILD_NUMBER} - ${JOB_NAME}",
                 body: "Attention: The pipeline failed during execution. Please check the logs immediately to resolve the issue: ${BUILD_URL}"
        }
    }
}


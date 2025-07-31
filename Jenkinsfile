pipeline {
    agent any
    
    environment {
        // Docker image names
        DOCKER_IMAGE = "dh-index-backend"
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_LATEST = "latest"
        
        // Docker registry (nếu sử dụng private registry)
        // DOCKER_REGISTRY = "your-registry.com"
        
        // Deployment directory (trong home directory để không cần sudo)
        DEPLOY_DIR = "${env.HOME}/dh-index-backend"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    // Build Docker image từ thư mục deploy
                    sh """
                        echo "Current directory: \$(pwd)"
                        echo "Listing files:"
                        ls -la

                        # Build Docker image từ thư mục deploy
                        cd deploy
                        echo "Building Docker image..."
                        docker build -f Dockerfile -t ${DOCKER_IMAGE}:${DOCKER_TAG} ..
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:${DOCKER_LATEST}
                    """
                }
            }
        }
        
        stage('Test Image') {
            steps {
                echo 'Testing Docker image...'
                script {
                    sh """
                        echo "Testing if image exists..."
                        docker images | grep ${DOCKER_IMAGE}

                        echo "Current build tag: ${DOCKER_TAG}"
                        echo "Checking if image ${DOCKER_IMAGE}:${DOCKER_TAG} exists..."
                        if docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "${DOCKER_IMAGE}:${DOCKER_TAG}"; then
                            echo "✅ Image found!"
                        else
                            echo "❌ Image ${DOCKER_IMAGE}:${DOCKER_TAG} not found!"
                            echo "Available images:"
                            docker images ${DOCKER_IMAGE}
                            exit 1
                        fi

                        echo "Testing basic container run..."
                        docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} python --version

                        echo "Testing Django installation..."
                        docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} python -c "import django; print('Django OK')"
                    """
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                script {
                    // Chạy container tạm để test (không dùng --rm để có thể debug)
                    sh """
                        echo "Creating test data directory..."
                        mkdir -p ${WORKSPACE}/test_data

                        echo "Starting test container..."
                        docker run -d --name test-backend-${BUILD_NUMBER} \
                            -p 8001:8000 \
                            -v ${WORKSPACE}/test_data:/app/data \
                            -e DATABASE_PATH=/app/data/db.sqlite3 \
                            ${DOCKER_IMAGE}:${DOCKER_TAG}

                        echo "Waiting for container to start..."
                        sleep 5

                        echo "Checking container status immediately..."
                        docker ps -a | grep test-backend-${BUILD_NUMBER} || echo "Container not found"

                        echo "Getting container logs..."
                        docker logs test-backend-${BUILD_NUMBER} 2>&1 || echo "No logs available"

                        echo "Waiting a bit more..."
                        sleep 10

                        echo "Checking if container is still running..."
                        if docker ps | grep -q test-backend-${BUILD_NUMBER}; then
                            echo "Container is running, testing health check..."
                            sleep 10

                            echo "Testing health check..."

                            # Try multiple endpoints
                            for i in {1..5}; do
                                echo "Attempt \$i/5..."
                                if curl -f http://localhost:8001/admin/ 2>/dev/null; then
                                    echo "✅ Health check successful!"
                                    break
                                elif curl -f http://localhost:8001/ 2>/dev/null; then
                                    echo "✅ Root endpoint accessible!"
                                    break
                                else
                                    echo "❌ Attempt \$i failed, waiting 5 seconds..."
                                    sleep 5
                                fi

                                if [ \$i -eq 5 ]; then
                                    echo "All health check attempts failed, showing container logs:"
                                    docker logs test-backend-${BUILD_NUMBER}
                                    echo "Container status:"
                                    docker ps -a | grep test-backend-${BUILD_NUMBER}
                                    echo "Network info:"
                                    docker port test-backend-${BUILD_NUMBER}
                                    exit 1
                                fi
                            done
                        else
                            echo "Container stopped unexpectedly!"
                            echo "Final container status:"
                            docker ps -a | grep test-backend-${BUILD_NUMBER}
                            echo "Final container logs:"
                            docker logs test-backend-${BUILD_NUMBER} 2>&1
                            echo "Container inspect:"
                            docker inspect test-backend-${BUILD_NUMBER} --format='{{.State.ExitCode}} {{.State.Error}}'

                            # Cleanup before exit
                            docker rm test-backend-${BUILD_NUMBER} || true
                            rm -rf ${WORKSPACE}/test_data || true
                            exit 1
                        fi

                        echo "Test successful, cleaning up..."
                        docker stop test-backend-${BUILD_NUMBER}
                        docker rm test-backend-${BUILD_NUMBER}
                        rm -rf ${WORKSPACE}/test_data
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying to production...'
                script {
                    sh """
                        # Tạo thư mục deploy và data nếu chưa có
                        mkdir -p ${DEPLOY_DIR}
                        mkdir -p ${DEPLOY_DIR}/data
                        mkdir -p ${DEPLOY_DIR}/logs

                        # Copy docker-compose file
                        cp deploy/docker-compose.prod.yml ${DEPLOY_DIR}/docker-compose.yml

                        # Stop old container
                        cd ${DEPLOY_DIR}
                        docker-compose down || true

                        # Start new container with updated image
                        docker-compose up -d

                        # Health check
                        sleep 20
                        curl -f http://localhost:8000/admin/ || exit 1
                    """
                }
            }
        }

        stage('Cleanup') {
            steps {
                echo 'Cleaning up old Docker images...'
                script {
                    sh """
                        echo "Current Docker images:"
                        docker images ${DOCKER_IMAGE}

                        echo "Cleaning up old images (keeping latest 2 versions)..."
                        # Xóa images cũ, chỉ giữ lại 2 bản gần nhất + latest
                        docker images ${DOCKER_IMAGE} --format "{{.Tag}}" | grep -E '^[0-9]+\$' | sort -nr | tail -n +3 | while read tag; do
                            echo "Removing ${DOCKER_IMAGE}:\$tag"
                            docker rmi ${DOCKER_IMAGE}:\$tag || true
                        done

                        echo "Cleaning up dangling images..."
                        docker image prune -f || true

                        echo "Final Docker images:"
                        docker images ${DOCKER_IMAGE}
                    """
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed!'
            // Dọn dẹp workspace nếu cần
            cleanWs()
        }
        success {
            echo 'Deployment successful!'
            // Có thể gửi notification thành công
        }
        failure {
            echo 'Pipeline failed!'
            // Có thể gửi notification lỗi
        }
    }
}

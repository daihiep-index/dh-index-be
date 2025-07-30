pipeline {
    agent any
    
    environment {
        // Docker image names
        DOCKER_IMAGE = "dh-index-backend"
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_LATEST = "latest"
        
        // Docker registry (nếu sử dụng private registry)
        // DOCKER_REGISTRY = "your-registry.com"
        
        // Deployment directory
        DEPLOY_DIR = "/opt/dh-index-backend"
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
                dir('dh_index') {
                    script {
                        // Build Docker image
                        sh """
                            cd deploy
                            docker build -f Dockerfile -t ${DOCKER_IMAGE}:${DOCKER_TAG} ..
                            docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:${DOCKER_LATEST}
                        """
                    }
                }
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                dir('dh_index') {
                    script {
                        // Chạy container tạm để test
                        sh """
                            docker run --rm -d --name test-backend-${BUILD_NUMBER} \
                                -p 8001:8000 ${DOCKER_IMAGE}:${DOCKER_TAG}
                            
                            # Đợi container khởi động
                            sleep 10
                            
                            # Test health check
                            curl -f http://localhost:8001/admin/ || exit 1
                            
                            # Dọn dẹp
                            docker stop test-backend-${BUILD_NUMBER}
                        """
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main' // Chỉ deploy khi push vào main branch
            }
            steps {
                echo 'Deploying to production...'
                script {
                    sh """
                        # Tạo thư mục deploy nếu chưa có
                        sudo mkdir -p ${DEPLOY_DIR}
                        
                        # Copy docker-compose file
                        sudo cp dh_index/deploy/docker-compose.yml ${DEPLOY_DIR}/
                        
                        # Stop old container
                        cd ${DEPLOY_DIR}
                        sudo docker-compose down || true
                        
                        # Remove old image
                        sudo docker rmi ${DOCKER_IMAGE}:${DOCKER_LATEST} || true
                        
                        # Start new container
                        sudo docker-compose up -d
                        
                        # Health check
                        sleep 15
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
                        # Xóa images cũ (giữ lại 3 bản gần nhất)
                        docker images ${DOCKER_IMAGE} --format "table {{.Tag}}" | grep -v TAG | grep -v latest | sort -nr | tail -n +4 | xargs -r docker rmi ${DOCKER_IMAGE}: || true
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

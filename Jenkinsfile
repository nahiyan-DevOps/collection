pipeline {
    agent {
        label any
    }

    environment {
        FLASK_IMAGE_NAME = "nahiyan83bjit/collections:flask_app"
        POST_IMAGE_NAME = "nahiyan83bjit/collections:post_app"
        MUSIC_IMAGE_NAME = "nahiyan83bjit/collections:music_app"
        DOCUMENTS_IMAGE_NAME = "nahiyan83bjit/collections:documents_app"
        KUBE_CONFIG_ID = "kubernetes-config"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: 'github-auth', url: 'https://github.com/nahiyan-DevOps/collection'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker images
                    dockerBuildImage(FLASK_IMAGE_NAME)
                    dockerBuildImage(POST_IMAGE_NAME)
                    dockerBuildImage(MUSIC_IMAGE_NAME)
                    dockerBuildImage(DOCUMENTS_IMAGE_NAME)
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Push Docker images to Docker Hub
                    dockerPushImage(FLASK_IMAGE_NAME)
                    dockerPushImage(POST_IMAGE_NAME)
                    dockerPushImage(MUSIC_IMAGE_NAME)
                    dockerPushImage(DOCUMENTS_IMAGE_NAME)
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Deploy to Kubernetes
                    deployToKubernetes()
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    // Remove Docker images
                    dockerRemoveImage(FLASK_IMAGE_NAME)
                    dockerRemoveImage(POST_IMAGE_NAME)
                    dockerRemoveImage(MUSIC_IMAGE_NAME)
                    dockerRemoveImage(DOCUMENTS_IMAGE_NAME)
                }
            }
        }
    }

    post {
        always {
            // Clean up or post-pipeline actions (e.g., notify team)
            cleanup()
        }
    }
}

// Custom functions for improved readability and reusability

def dockerBuildImage(imageName) {
    def image = docker.build imageName
    // Custom steps for building the Docker image (if needed)
}

def dockerPushImage(imageName) {
    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub') {
        def image = docker.image(imageName)
        image.push()
    }
}

def dockerRemoveImage(imageName) {
    sh "docker rmi $imageName"
}

def deployToKubernetes() {
    kubeconfig(credentialsId: env.KUBE_CONFIG_ID, serverUrl: '192.168.56.20') {
        sh '/usr/bin/kubectl apply -f collections.yml'
        // Custom deployment steps (e.g., check rollout status, handle errors)
    }
}

def cleanup() {
    // Perform any cleanup actions after the pipeline execution is complete
    // (e.g., delete temporary files or resources)
    deleteDir()
}

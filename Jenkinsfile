pipeline {
    agent any

    environment {
        FLASK_IMAGE_NAME = "nahiyan83bjit/collections:flask_app"
        POST_IMAGE_NAME = "nahiyan83bjit/collections:post_app"
        MUSIC_IMAGE_NAME = "nahiyan83bjit/collections:music_app"
        DOCUMENTS_IMAGE_NAME = "nahiyan83bjit/collections:documents_app"
        KUBE_CONFIG_ID = "kubernetes-config"
    }

    stages {
        stage('Git') {
            steps {
                git branch: 'main', credentialsId: 'github-auth', url: 'https://github.com/nahiyan-DevOps/collection'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    flaskImage = docker.build FLASK_IMAGE_NAME
                    postImage = docker.build POST_IMAGE_NAME
                    musicImage = docker.build MUSIC_IMAGE_NAME
                    documentsImage = docker.build DOCUMENTS_IMAGE_NAME
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Push the Docker image to Docker Hub
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub') {
                        flaskImage.push()
                        postImage.push()
                        musicImage.push()
                        documentsImage.push()
                    }
                }
            }
        }

        stage('Deploy stage') {
            steps {
                echo 'This is deploy stage'
                script {
                    kubeconfig(credentialsId: env.KUBE_CONFIG_ID, serverUrl: '192.168.56.20') {
                        sh '/usr/bin/kubectl apply -f collections.yml'
                    }
                }
            }
        }
    }
}
pipeline {
    agent any

    environment {
        EC2_USER = 'ec2-user'
        EC2_HOST = '16.170.140.55'
        PRIVATE_KEY_PATH = 'C:/Users/Success/Downloads/electricaa-key.pem'
        IMAGE_NAME = 'hub_electricaa'
        IMAGE_TAG = "build-${env.BUILD_NUMBER}"
        GIT_REPO = 'https://github.com/Success-C-Opara/electric-001.git'
        BRANCH_NAME = 'main'
        GIT_BASH = '"C:\\Program Files\\Git\\bin\\bash.exe" -c'
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub-creds'
    }

    stages {
        stage('Clone Code') {
            steps {
                echo "✅ Cloning '${BRANCH_NAME}' from ${GIT_REPO}"
                git branch: "${BRANCH_NAME}", url: "${GIT_REPO}"
            }
        }

        stage('Docker Build, Push & Deploy') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKERHUB_CREDENTIALS_ID}",
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_PASS'
                )]) {
                    echo "🐳 Logging into DockerHub"
                    bat """
                        ${GIT_BASH} "echo '${DOCKERHUB_PASS}' | docker login -u '${DOCKERHUB_USER}' --password-stdin"
                    """

                    echo "🐳 Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                    bat """
                        ${GIT_BASH} "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                    """

                    echo "📤 Pushing Docker image to DockerHub"
                    bat """
                        ${GIT_BASH} "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    """

                    echo "🚀 Deploying to EC2: ${EC2_HOST}"
                    script {
                        def remoteScript = """
                            echo '${DOCKERHUB_PASS}' | docker login -u '${DOCKERHUB_USER}' --password-stdin && \
                            docker pull ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} && \
                            docker stop ${IMAGE_NAME} || true && \
                            docker rm ${IMAGE_NAME} || true && \
                            docker run -d --name ${IMAGE_NAME} -p 80:80 ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                        """.stripIndent().trim()

                        // Escape for one-liner SSH inside Git Bash
                        def escapedScript = remoteScript.replace("'", "'\\''")

                        def sshCommand = """
                            ${GIT_BASH} "ssh -o StrictHostKeyChecking=no -i '${PRIVATE_KEY_PATH}' ${EC2_USER}@${EC2_HOST} '${escapedScript}'"
                        """.stripIndent().trim()

                        bat sshCommand
                    }
                }
            }
        }
    }
}

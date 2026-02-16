pipeline {
    agent any

    environment {
        DOCKER_HOST = 'tcp://localhost:2375'
        DOCKER_CLIENT_TIMEOUT = '300'
        COMPOSE_HTTP_TIMEOUT = '300'
        DOCKER_BUILDKIT = '1'
        EC2_USER = 'ec2-user'
        EC2_HOST = '44.202.43.138'
        PRIVATE_KEY_PATH = '/c/Users/OMALE/Downloads/successkey1.pem'
        IMAGE_NAME = 'success-saas-jen1'
        IMAGE_TAG = "build-${env.BUILD_NUMBER}"
        GIT_REPO = "https://github.com/omale101/saas2-pro.git"
        BRANCH_NAME = 'main'
        GIT_BASH = '"C:\\Program Files\\Git\\bin\\bash.exe" -c'
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub-creds'
    }

    stages {
        stage('Clone Code') {
            steps {
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
                    bat """
                        ${GIT_BASH} "echo '${DOCKERHUB_PASS}' | docker login -u '${DOCKERHUB_USER}' --password-stdin"
                        ${GIT_BASH} "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                        ${GIT_BASH} "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    """

                    script {
                        def remoteScript = """
                            echo '${DOCKERHUB_PASS}' | docker login -u '${DOCKERHUB_USER}' --password-stdin && \
                            docker pull ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} && \
                            docker stop ${IMAGE_NAME} || true && \
                            docker rm ${IMAGE_NAME} || true && \
                            docker run -d --name ${IMAGE_NAME} -p 80:80 ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                        """.stripIndent().trim()

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

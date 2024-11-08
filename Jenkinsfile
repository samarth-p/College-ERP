pipeline {
    agent any
    
    
    environment {
        SCANNER_HOME=tool 'sonar6.2'
        imageName = "neeraj46665/erp"
       
    }
    parameters {
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Enter Docker image tag')
    }
   
    
    stages {
        stage ("clean workspace") {
            steps {
                cleanWs()
            }
        }
        stage ("Git Checkout") {
            steps {
                git url: "https://github.com/galgotiasuniversity1/College-ERP.git", branch: "master"
            }
        }
        stage("Sonarqube Analysis"){
            steps{
                withSonarQubeEnv('sonarserver') {
                    
                    sh '''$SCANNER_HOME/bin/sonar-scanner -Dsonar.projectName=ERP -Dsonar.projectKey=ERP -Dsonar.verbose=true
'''
                }
            }
        }
        stage("Code Quality Gate"){
          steps {
                script {
                    waitForQualityGate abortPipeline: false, credentialsId: 'Sonar-token' 
                }
            } 
        }
        
        stage ("Build Docker Image") {
            steps {
                sh "docker build -t ${imageName}:${params.IMAGE_TAG} ."
            }
        }
        stage ("Push to DockerHub") {
            steps {
                script {
                    withDockerRegistry(credentialsId: 'dockerlogin') {
                       
                        sh "docker push ${imageName}:${params.IMAGE_TAG}"
                    }
                }
            }
        }
        
        stage ("Update Kubernetes Manifest") {
            steps {
                script {
                    // Update the image tag in deployment.yaml
                    dir("/var/lib/jenkins/workspace/jenkins-cicd/k8s") {
                        sh """
                            
                            sed -i 's|image: neeraj46665/erp:[^[:space:]]*|image: neeraj46665/erp:${params.IMAGE_TAG}|' deployment.yml

                          
                        """
                    }
                }
            }
        }


        
        stage ("Git Commit and Push") {
            steps {
                withCredentials([usernamePassword(credentialsId: 'Github-cred', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                    script {
                        sh """
                        git config user.name "neeraj"
                        git config user.email "na46665@gmail.com"
                        git add k8s/deployment.yml
        
                        # Check if there are changes to commit
                        if git diff --cached --quiet; then
                            echo "No changes to commit."
                        else
                            git commit -m "Update image tag to ${params.IMAGE_TAG}"
                            git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/galgotiasuniversity1/College-ERP.git master
                        fi
                        """
                    }
                }
            }
        }


        stage ("Trigger ArgoCD Sync") {
            steps {
                echo "ArgoCD will detect the change and sync the application automatically."
            }
        }
        
    
    }
    post {
        success {
            echo "Pipeline completed successfully! All stages passed."
            // Add any additional success notifications, e.g., email or Slack
        }
        
        failure {
            echo "Pipeline failed. Check the logs for more details."
            // Add any additional failure notifications, e.g., email or Slack
        }
        
        
    }
    
    
}

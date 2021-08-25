pipeline {
    agent any
    environment {
        DOCKER_IMAGE_NAME = "mandeep1690/serviceb"
 	dockerfile= "Dockerfile"   
}
    stages {
        stage('Build') {
            steps {
                echo 'Running build automation'
            }
        }
        stage('Build Docker Image') {
            when {
                branch 'main'
            }
            steps {
                script {
		    app = docker.build(DOCKER_IMAGE_NAME, "-f serviceB/${dockerfile} .")
                    app.inside {
                        sh 'echo Hello, World!'
                    }
                }
            }
        }
        stage('Push Docker Image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockercred') {
                        app.push("${env.BUILD_NUMBER}")
                        app.push("latest")
                    }
                }
            }
        }
        stage('DeployToProduction') {
            when {
                branch 'main'
            }
            steps {
///                input 'Deploy to Production?'
                milestone(1)
		script {
		   sh """
			/usr/local/bin/helm upgrade --install servicea-app serviceB/helm-charts/appserviceb/ --values serviceB/helm-charts/appserviceb/values.yaml --set image.tag="${env.BUILD_NUMBER}" --kubeconfig  /home/cloud_user/.kube/config
		"""
		}
                //implement Kubernetes deployment here
//        	kubernetesDeploy(kubeconfigId: 'kubeconfig',
//                        configs: 'serviceA/kube-manifests/deployment.yaml',
//                        enableConfigSubstitution: true
//			)
		}
        }
    }
}

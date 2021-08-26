## adi-serviceb
This service B calls service A and prints out to stdout whenever 500 is returned.
## Prerquisites
* Kubernetes - Tested on version 1.10 and latest(1.21)
* Helm3
* Jenkins - v2.249.3 ( with plugins : Pipeline: Declarative(1.9.1) and GitHub, Generic Webhook Trigger Plugin (1.75)
## Setup Jenkins Jobs
* Add github and docker credentials in jenkins - dockercred and githubcred to run the pipeline
* Create 2 jobs - adi-serviceA and adi-seviceB
* Add github in sourcescm
* Add Jenkins webhook in github
## Install and Deploy
* Helm Charts of service is created at https://github.com/imkaur/adi-serviceb/tree/main/serviceB/helm-charts/appserviceb
* Jenkins acts as orchestrator to deploy the application in kubernetes.
* There is no requirement for this service to be exposed to external network, hence, clusterIP service has been used as default.
* If you wish to expose it to external network, you can change the type in values.yaml to NodePort or LoadBalancer (Eg. Type: NodePort)
## Docker Image
* If I used a python3.7 image, the iamge size turns out to be 918MB which is huge.
* To reduce the size and minimize the attack surface below steps are taken:
  * Multi-stage docker build 
  * Considered python:3.7-alpine image as base
## CronJob
To create a scheduled job for calling service B, perform below step in kubernetes cluster:
* kubectl apply -f cronjob.yaml
## Monitoring
* Service is monitored from kuberenets perspective by setting monitoring probes such as - startupProbe, livenessProbe and readinessProbe.
* To get insights about the applictaion, it can be monitored by exposing the metrics to prometheus and alert can be set when error ratio is greater than threshold limit.
* The application error percentage is the number of requests that result in an error compared to the total number of requests.
* Initialize prometheus metrics by prometheus client library. It is possible to import prometheus metrics from prometheus_flask_exporter and get request counters exposed to /metrics endpoint.
* flask_http_request_total - Total number of HTTP requests by method and status
* Add a rule to alertmanager with value such as => rate(flask_http_request_total{status="500"}[1m]) > 60


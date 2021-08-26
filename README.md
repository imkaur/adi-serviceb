## adi-serviceb
This service B calls service A (src- https://github.com/imkaur/adi-servicea) and prints out to stdout whenever 500 is returned.
## Prerquisites
* Kubernetes - version 1.21
* Helm3
* Jenkins - v2.249.3 
 * with plugins : 
   * Pipeline: Declarative(1.9.1) 
   * If you want to trigger via webhook install - GitHub and Generic Webhook Trigger Plugin (1.75)
## Setup Jenkins Jobs
* Add github and docker credentials in jenkins - dockercred and githubcred to run the pipeline
* Create 2 jobs - adi-serviceA and adi-seviceB
* Add github in sourcescm
* Add Jenkins webhook in github
## Docker Image
* Docker build versioning is in place and every push generates a new build image tag.
* If I used a python3.7 image, the iamge size turns out to be 918MB which is huge.
* To reduce the size and minimize the attack surface below steps are taken:
  * Multi-stage docker build
  * Considered python:3.7-alpine image as base
  * Current size of service A image is 89.7MB
## Install and Deploy
* Helm Charts of service is created at https://github.com/imkaur/adi-serviceb/tree/main/serviceB/helm-charts/appserviceb
* Jenkins acts as orchestrator to deploy the application in kubernetes.
* There is no requirement for this service to be exposed to external network, hence, clusterIP service has been used as default.
* If you wish to expose it to external network, you can change the type in values.yaml to NodePort or LoadBalancer (Eg. Type: NodePort)
* If you wish to deploy without use of Jenkins and from latest image:
  * `helm upgrade --install servicea-app serviceA/helm-charts/appserviceb/ --values serviceB/helm-charts/appserviceb/values.yaml --set image.tag=latest`
## CronJob
To create a scheduled job for calling service B, perform below step in kubernetes cluster:
* kubectl apply -f cronjob.yaml
## Monitoring
* Service is monitored from kubernetes perspective by setting monitoring probes such as - startupProbe, livenessProbe and readinessProbe.
* Out of the many ways, one of the standard way of monitoring applications is by using a combination of prometheus, grafana and alert-manager. While prometheus scrapes the target by pulling the metrics, grafana displays dashboards and alertmanager is being used to generate alerts to send to email, on-call notification systems, and chat platforms.
* Here, to get insights about the applictaion, it can be monitored by exposing the metrics to prometheus and alert can be set when error ratio is greater than threshold limit. 
* The application error percentage is the number of requests that result in an error compared to the total number of requests.
* Initialize prometheus metrics by prometheus client library. It is possible to import prometheus metrics from prometheus_flask_exporter and get request counters exposed to /metrics endpoint.
* Assuming http_request_total - gives Total number of HTTP requests processed and http_status_500_total which gives the total unexpected errors in our application.
* A rule like below can give the error ratio
  * `rate(http_status_500_total [1m]) / rate(http_request_total [1m])`
* If this comes out to be > threshold_value, we can trigger an alert to the preferred group and channel via alert manager.

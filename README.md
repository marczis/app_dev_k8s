# Simple application development and deployment for K8s
The purpose of this "training" is to give you an overview of the application development workflow for Kubernetes.
During this session, you will:
 - Create a simple REST API server application with Python
 - In a docker container
 - Test it locally
 - Push it into a container registry
 - Deploy it into a kubernetes cluster (mine running on GCP)
 - Expose it to the world
 - Scale it up / down manually
 - Roll out upgrades

Future things I willing to add to this training:
  - Building a CI/CD pipeline for your software
  - Setup auto scaling


## Pre-requirements
 - You understand python code
 - You familiar with REST API-s in general
 - You able to install the next tools:
   - docker
   - kubectl
   - python
 - I made the training on Linux / Fedora, but nothing keeps you from repeat the whole process on Mac or Windows - if you do soo, feel free to add the steps and make a pull request ;)

## Table of contents

| Chapter | Title | Link |
|---------|-------|----- |
|    1    | Developing a simple REST service |[Jump](./Chapter-1/Chapter1.md) |
|    2    | Packing your application into a docker image |[Jump](./Chapter-2/Chapter2.md) |
|    3    | Deploy your application to K8s |[Jump](./Chapter-3/Chapter3.md) |
|    4    | Rolling out a new version | [Jump](./Chapter-4/Chapter4.md) |

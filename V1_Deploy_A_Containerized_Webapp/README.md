# Deploy a docker image on AWS Fargate

This tutorial deploys a basic streamlit app on AWS Farget.

 - reference: https://www.youtube.com/watch?v=1_AlV-FFxM8


Deploy a webapp on AWS ECR/ECS using Docker
- First write an streamlit app.
- Create an image of the app using Docker.
- Create a repository in ECR. ideally a single repository should contains different versions of the image for the same service, task.
- Push the image to the repository.
- Create a Fargate cluster in ECS.
- Create a task definition in ECS.
- Create a service in ECS.
- If unable to accesss the app using public IP. Follow the document provided in VPC directory.

ECR - Elastic Container Registry
ECS - Elastic Container Service


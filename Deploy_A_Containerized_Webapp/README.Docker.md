# Deploy a webapp on AWS ECR/ECS using Docker
- First write an streamlit app that provides a facility to QnA over PDF documents.
- Create an image of the app using Docker.
- Create a repository in ECR. ideally a single repository should contains different versions of the image for the same service, task.
- Push the image to the repository.
- Create a Fargate cluster in ECS.
- Create a task definition in ECS.
- Create a service in ECS.
- If unable to accesss the app using public IP. Follow the document provided in VPC directory.

 - reference: https://www.youtube.com/watch?v=1_AlV-FFxM8

ECR - Elastic Container Registry
ECS - Elastic Container Service

## Docker
### Docker Get Started
https://docs.docker.com/get-started/

### Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:8000.

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.
'docker buildx build . --platform linux/x86_64 -t streamlit_image_linux'

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)


### Persistent Storage
Data can not be stored in docker container. It will be lost when container is stopped. 
To store the data persistently, you need to use the local directory that is mount on the
containers path.
 > docker run -p 80:8501 -v /Users/vss/Personal/Git/Learning_LLM/QnA_Over_Text_Documents/uploaded_pdfs:/app/data streamlit_image

### Connecting to localhost of host from docker.
Network stack of the host machine and docker is different due to being different entity.
To connect to the localhost of the host machine from the docker container, there are multiple ways.
one way is to use host.docker.internal as dns name instead of localhost in url.
https://www.youtube.com/watch?v=lJAhaiDuAYc

## Deploy the docker container on the remote machine
- Install docker engine on the remote machine. (https://docs.docker.com/engine/install/)

docker run -p 8083:8505 -v /mnt/sasdshare/vivek/LLM/llm_apps/QnA_Over_Text_Documents/uploaded_pdfs:/app/data streamlit_image

## Run ollama on docker
  - Pulls the image from docker registry and creates a container on the host system 
  - `sudo docker run -d --name ollama -p 11434:11434 -v ollama_storage:/root/.ollama  ollama/ollama:latest` 
  - Adding OLLAMA_HOST env variable with 0.0.0.0 value, any IP address in home network can access it.
  - `OLLAMA_HOST=0.0.0.0:11434 sudo docker run -d --name ollama -p 11434:11434 -v ollama_storage:/root/.ollama  ollama/ollama:latest`
  - Pulls model 
  - `sudo docker exec -it ollama ollama run deepseek-r1:1.5b`


## Important notes:
* login before runing the docker-compose command. Use docker loing -u vsscorvc 
* Never put comment in the same line that of code in the Dockerfile. It will cause the build to fail. Use separate line for comments and codes.
* For CMD, use the form ["executable", "param1", "param2"] and in double quotes.

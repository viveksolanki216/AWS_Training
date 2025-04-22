# Deploy a docker image on AWS EC2 instance.

This tutorial deploys a basic streamlit app on AWS EC2 instance that internally access ollama service. 
 - Streamlit App: A basic chat app that question and answer over a uploaded pdf using local llm.
 - Ollama: A local llm service that can be used to run the llm models locally.
 - Both apps are running over docker in the same EC2 instance.
 - Setting up an EC2 instance with Nvidia GPU to run the ollama service.

References:
- https://www.youtube.com/watch?v=_k1pzkqq_rw&t=2168s

#### Ollama works faster/like realtime on GPU.
 - Ollama uses GPU in background. It works really well on Mac-Silicon GPU.
 - When running ollama on docker (i.e. with docker composer), it's unable to use GPU. and runs very slow.

**Points to note:**
- Ollama service will not be able to acces using "host.docker.internal:11434" in the streamlit app, because ollama is running over a container and you need to provie the private ip address of the EC2 instance.
- You need to add the inbound rule  with port number and add "0.0.0.0/0" in the security group to allow public access to the app.
- You need to install the nvidia driver, utils, container toolkit, docker, docker-compose on the EC2 instance.
- You need to create a repository in ECR and push the docker image to ECR and add a policy for EC2 instance for ECR access.

## Steps:
### Create an app and docker image:
- Create a streamlit app that uses ollama service to run the llm models locally
- Create a docker image of the app using Dockerfile.
- Use following: Go to Learning_LLM repository and go to "LLM_Over_Text_Documents" directory.

### Create EC2 Instance:
- "Launch Instance" in AWS console under EC2 & Fill necessary details.
- Select the Basic AMI or operating system image "Ubuntu Server 24.04 LTS (HVM),EBS General Purpose (SSD) Volume Type"
- Select "g4dn.2xlarge" instance that has T4 Nvidia GPU to run for ollama.
- Select Key-pair name to connect to the instance. This key-pair should exist in your local machine.
- Network-settings: 
  - Select a VPC that has a public subnet, with internet gateway and router table.
  - Auto Assign Public IP: Enable
  - "Create a security group", but configure it later for public access.
- Configure Storage: Bump up it to 50GB
- And launch the instance.
- Click "Connect" button to get the SSH command to connect to the instance.
- SSH into the instance using the command provided in the console. i.e. ssh -i "MyKeyPair2.pem" ubuntu@10.0.0.24

### Configure the EC2 Instance Environment:
You need to install the required drivers, utils for the Nvidia GPU. Otherwise ollama will not be able to use the GPU.
We will install nvidia-driver, nvidia-utils (necessary for GPU support), nvidia-container-toolkit (necessary for GPU support in docker),
docker, docker-compose, btop (activity monitor).

- To check the GPU type `sudo lshw -C display`
- To install the activity monitor `sudo snap install btop`
- Install the nvidia driver: `sudo apt-get install nvidia-driver-550-server --yes` or nvidia-driver-550
- Install the nvidia utils: `sudo apt-get install nvidia-utils-550-server --yes` or nvidia-utils-550
- Make sure version of driver and utils shoule be same or else it will raise an error.
- To check the GPU driver version `sudo nvidia-smi`
- Now install the nvidia container toolkit, that will enable the GPU support for the docker processes. 
  - https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
- Install docker engine, `sudo apt-get install docker.io --yes`
- Just check for an example, that we are able to access GPU from docker.
  - `sudo docker run --rm -it --gpus=all ubuntu` --rm = remove the container after exit, -it = interactive terminal
  - you wil be able to see Testl Tg GPU when you run `nvidia-smi` inside the above ubuntu running on the container.
  - `exit`
- Install docker-compose plugin https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository.

### Push the local app docker image to ECR.
Create a repository in ECR and push the docker image to ECR. From where we can pull the image to run on the EC2 instance.
- Create a repository in ECR using console
- Tag the local image with the ECR repository URI `docker tag image_name account_id.dkr.ecr.us-east-1.amazonaws.com/repository_name:latest`
- Login to AWS ECR `aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 205930620783.dkr.ecr.us-east-1.amazonaws.com` 
- docker push 205930620783.dkr.ecr.us-east-1.amazonaws.com/qna_streamlit_ollama:latest

### Now compose a docker-compose.yml file to run the app.


### Not able to pull the image from ECR into the EC2 instance.
Because EC2 instance is not allowed to access the ECR repository. So we need to attach a role to the EC2 instance that has access to ECR.
Or you can setup aws cli on the EC2 instance and login to ECR using the aws cli and the docker pull the image.
 - First generate keys as shown in the video https://www.youtube.com/watch?v=pEUuJiIGtqk&list=PLqoUmUbJ_zDHPwK-ZWATXiYrUXwWkLY65&index=5
   - Go to IAM -> Users -> vivek -> Security credentials -> Create access key
 - `aws configure` and the fill in the keys as asked.
 - To authentic docker to an amazon ECR registry: `aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 205930620783.dkr.ecr.us-east-1.amazonaws.com`
 - After login succeded. 
 - Even if I try to pull the image using the docker command, it will not work. Because the EC2 instance is not allowed to access the ECR repository.

Instead, save the image in the tar file using 
 - `docker save -o llm_qna_docs.tar llm_qna_docs:linux_x86_64_4ec2`  
 - `scp -i "MyKeyPair2.pem" 'llm_qna_docs.tar' ubuntu@54.210.81.53:/home/ubuntu/llm_app`
 - `sudo docker load -i llm_qna_docs.tar`
 - `sudo docker images`

### Add inbound rule in the security group under EC2 instances for the public access to the app

### Pull the models in the ollama
 - `sudo docker exec -it llm_app-ollama-1 ollama pull deepseek-r1:7b`
 - `sudo docker exec -it llm_app-ollama-1 ollama pull mxbai-embed-large`

### To stop the app
- `sudo docker compose stop`

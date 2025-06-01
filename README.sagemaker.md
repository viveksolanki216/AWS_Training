
## Amazon SageMaker AI
Amazon SageMaker AI is a fully managed machine learning (ML) service. With SageMaker AI, data scientists and developers
can quickly and confidently build, train, and deploy ML models into a production-ready hosted environment. 
It provides a UI experience for running ML workflows that makes SageMaker AI ML tools available across multiple 
integrated development environments (IDEs).

reference: [AWS SageMaker Examples ReadTheDoc](https://sagemaker-examples.readthedocs.io/en/latest/intro.html)

You have several options for how you can use Amazon SageMaker.
 - IDE: SageMaker Studio
 - Console: SageMaker Notebook Instances
 - Command line & SDK: AWS CLI, boto3, & SageMaker Python SDK
 - 3rd party integrations: Kubeflow & Kubernetes operators

### [Setup SageMaker Domain](https://docs.aws.amazon.com/sagemaker/latest/dg/gs-studio-onboard.html)
Go to Amazon SageMaker AI, click on `Create Domain` and select single user domain. It will take 10-15 minutes to create the domain.
SageMaker Domain is a managed environment for data science and machine learning. It provides Jupyter notebooks, JupyterLab,
and other tools for data science and machine learning.

In SageMaker AI, a domain is an environment for your team to access SageMaker resources. A domain consists of a list of 
authorized users and users within a domain can share notebook files and other artifacts with each other. One account can
have either one or multiple domains.

### After creating the domain, create User Profile if not already created.

### [SageMaker Studio](http://sagemaker-examples.readthedocs.io/en/latest/aws_sagemaker_studio/index.html)
The first fully integrated development environment (IDE) for machine learning on AWS. Its mostly a collection of different
tools and/or IDE.

### Jupyter Lab Space
It's an IDE available in SageMaker Studio.
JupyterLab is a web-based interactive development environment for Jupyter notebooks, code, and data. You need to create
a Jupyter Lab Space that will ask you a server (EC2 instance) type that suits your needs, and on which this Lab Space 
will run. And also input a docker image that will have pre-installed python libraries and other dependencies installed.

### SageMaker Notebook
SageMaker Notebook is a fully managed service that provides a Jupyter notebook instance in the cloud. It is pre-configured
with the most popular data science libraries (e.g., TensorFlow, PyTorch, MXNet, Chainer, and Keras) and can be used to
build, train, and deploy machine learning models.

### EFS: Elastic File System
The memory where notebooks reside inside jupyter lab space is called EFS. It is a costly service, so it is recommended to
store the large files in S3 and then load them in the notebook.

### S3: Simple Storage Service
Amazon S3 is an object storage service that offers industry-leading scalability, data availability, security, and performance.

### Sagemaker Estimators
#### Using SageMaker Estimators
Estimators are high level interface (API) for training. It makes it very easy to train a model v/s doing it manually. 
 - What algorithm or framework to use
 - What script or Docker container
 - What compute resources
 - Where to store data and model artifacts

##### Types
 - **Built-in Algorithms:** These uses Sagemaker optimized containers for popular ML algo, no training scripts are needed. i.e. LinearLearner, XGBoost, KMeans
 - **Framework-Estimatoes:** (Script Mode): Use your own training script with a pre-built container for popular ML/DL frameworks. i.e. PyTorch, Tensorflow, SKLearn, HuggingFace
 - **Custom Containers:** Use any docker image you create. Gives full control. i.e Estimator
 - **Automatic Model Tuning:** Wrap any Estimtor with a HyperparameterTuner
 - **Local Model:** Almost all Estimators can run in "local model" just give "instance_type='local'". 

#### Why using a Sagemaker Estimators?
- Managed Training Infrastructure
    - You don't need to: Provision an EC2 instance, SSH into them, install package manually and cleanup, retire after the work is done. This is all managed by Estimators.
- Automatic S3 handling: No need to manually output data to S3, just provide the s3 location
- Reproducibility and Portability:
    - The Estimator keeps track of docker-image, instance-type/count, hyperparams, s3 paths, training code locations.
    - Makes it easy to re-run training, audit results, share configurations.
- Training at Scale:
    - Train on multiple instances, specify instance count.
    - SPOT instances. GPUs
    - Distribute Trainings
    - You don't want to script EC2 cluster provisioning yourself every time.
- Easy deployment Integration:
    - `predictor = estimator.deploy(initial_instance_count=1, instance_type='ml.m5.large')` creates a fully managed HTTPS inference endpoint with scaling, logging, and monitoring.
    - If you train manually, deploying to production becomes a manual DevOps task.

#### Notes while using Estimators:
- Training scripts (running on any instance):
   - Can read files from a s3 location
   - But can't write them. We need to write the output files into the container hosted on the training/EC2 instance itself and manually write/upload the files using s3 objects.
   - Or just use the default location '/opt/ml' of the instance mentioned in different environment variables i.e. "SM_MODEL_DIR" = '/opt/ml/model' for model output, "SM_OUTPUT_DATA_DIR" = 'opt/ml/output/data/' for output data.
   - Sagemaker collects everything in '/opt/ml/model', compresses it and upload it to s3 location specified in the Estimator
### Issues Arised and Resolved
#### Couldn't access/read files from user/new created buckets.
Reason being S3 read access was not allowed for the role that is executing the code.
- Role: Role is kind of a hat that a user assumes to execute a task. It contains all the necessary permissions to resources needed to execute the task.
- Policy: each role has a policy attached as a json document, which we can edit to give necessary permissions or there are pre-defined policies that can be used.
i.e. for this issue, just display the role using `get_execution_role(sagemaker_session=sagemaker.Session())`, and attach the aws managed policy to "AmazonS3FullAccess" to the role. This will give access to all the buckets for the current user. Or if you want to give
access to a selected bucket either edit the policy attached to the role or create a custom managed policy.


{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Action": [
				"s3:ListBucket"
			],
			"Effect": "Allow",
			"Resource": [
				"arn:aws:s3:::SageMaker",
				"*"
			]
		},
		{
			"Action": [
				"s3:GetObject",
				"s3:PutObject",
				"s3:DeleteObject"
			],
			"Effect": "Allow",
			"Resource": [
				"arn:aws:s3:::SageMaker/*",
                "arn:aws:s3:::{bucket_name}/*",
			]
		}
	]
}




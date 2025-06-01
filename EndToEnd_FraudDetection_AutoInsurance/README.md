
# End to End ML Project - Fraud Detection Auto Insurance.
Reference: https://github.com/aws/amazon-sagemaker-examples/blob/4534bff4b5b5062af5789d98c4ddca01b0cb5d1f/end_to_end/fraud_detection/0-AutoClaimFraudDetection.ipynb

Steps:
1. Data Processing Using Sagemaker Data Wrangler



## SageMaker DataWrangler 

 - It simplifies the data preparation process by providing a visual interface for data exploration, transformation, and feature engineering. 
 - 300 built in transformations without any code.
 - Genrates data quality reports.
 - Scale to preocess petabytes of data.
 - Data preperation in minutes, Low code
 - Understand your data with visualizations




SageMaker Processing - docs
SageMaker Feature Store- docs
SageMaker Clarify- docs
SageMaker Training with XGBoost Algorithm and Hyperparameter Optimization- docs
SageMaker Model Registry- docs
SageMaker Hosted Endpoints- predictors - docs
SageMaker Pipelines- docs


## Sagemaker Estimators
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
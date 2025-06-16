
# End to End ML Project - Fraud Detection Auto Insurance.

References: 
- https://sagemaker-examples.readthedocs.io/en/latest/end_to_end/fraud_detection/1-data-prep-e2e.html

Steps:
1. Data Exploration in Jupyter Notebook
2. Data Processing Using Sagemaker Data Wrangler
3. Train Model using Custom Training Job (Script Mode)
4. Bias Checks using Sagemaker Clarify
5. Model Registry, Deploy on Endpoint and Predictions
6. Create an End to End Pipline using Sagemaker Pipeline


## 0. Data Exploration
### Using Jupter Lab (Notebook)

## 1. Data Processing 
### SageMaker DataWrangler 

 - It simplifies the data preparation process by providing a visual interface for data exploration, transformation, and feature engineering. 
 - 300 built in transformations without any code.
 - Genrates data quality reports.
 - Scale to preocess petabytes of data.
 - Data preperation in minutes, Low code
 - Understand your data with visualizations

## 2. Training - Custom Training Job (Script Mode)

### Sagemaker Estimators
#### Using SageMaker Estimators
Estimators are high level interface (API) for training. It makes it very easy to train a model v/s doing it manually. 
 - What algorithm or framework to use
 - What script or Docker container
 - What compute resources
 - Where to store data and model artifacts

##### Different Modes for Training Jobs
 - **Built-in Algorithms:** These uses Sagemaker optimized containers for popular ML algo, no training scripts are needed. i.e. LinearLearner, XGBoost, KMeans
 - **Framework-Estimatoes:** (Script Mode): Use your own training script with a pre-built container for popular ML/DL frameworks. i.e. PyTorch, Tensorflow, SKLearn, HuggingFace
 - **Custom Containers:** Use any docker image you create. Gives full control. i.e Estimator
 - **Automatic Model Tuning:** Wrap any Estimtor with a HyperparameterTuner
 - **Local Model:** Almost all Estimators can run in "local model" just give "instance_type='local'". 

##### Why using a Sagemaker Estimators?
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

##### Notes while using Estimators:
- Training scripts (running on any instance):
   - Can read files from a s3 location
   - But can't write them. We need to write the output files into the container hosted on the training/EC2 instance itself and manually write/upload the files using s3 objects.
   - Or just use the default location '/opt/ml' of the instance mentioned in different environment variables i.e. "SM_MODEL_DIR" = '/opt/ml/model' for model output, "SM_OUTPUT_DATA_DIR" = 'opt/ml/output/data/' for output data.
   - Sagemaker collects everything in '/opt/ml/model', compresses it and upload it to s3 location specified in the Estimator

###### Directory Structure inside script mode container.
/opt/ml/

├── input/

│   ├── config/           # Input config files (hyperparams, resource config)

│   ├── data/

│   │   ├── train/        # Your input channel

│   │   └── validation/   # Another channel

├── model/                # Where to save trained model

├── output/               # For evaluation metrics or custom output

One Can access the train channel inside the script as `os.environ.get("SM_CHANNEL_TRAIN")` or directly harcoding the path as '/opt/ml/input/data/train'.

## 3. Bias Checks Using Sagemake Clarify


## 4. Model Registry, Deploy on Endpoint
https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html

- Create a model-package group
- Create a model-package using training job (this will create a model in "Registered Models")
- Deploy the model on an endpoint (this will create a model in "Deployable Models")

### Model Package Group: 
A collection of different version of the same model (not exactly same, but different models for same problem statements).
### Model Package:
A particular version of the model.
### Model Registry Collections:
https://docs.aws.amazon.com/sagemaker/latest/dg/modelcollections.html

Similar to directories, for better discovery of models they can be organized in differnt collections (could be nested). Different models for same domain of problem can go in one collection i.e. same model algorithms/architeture i.e. NLP Models, Speech Recognition Models. Transformer Models etc.


## 5. Make Predictions

- From a real-time inference endpoint
   - Using the sagemaker.predictor.Predictor
   - Using the sagemaker.xgboost.model.XGBoostPredictor
   - Using an inference script.
- Batch Prediction using Batch Transform


# 6. End to End Pipeline

## Why Each Step Runs Separately in a SageMaker Pipeline

In SageMaker Pipelines, each step is executed as a **separate process**, usually on a **different instance**, using its own **container**. This may seem unnecessary at first — why not run all steps on a single machine? Here's why this design is actually powerful and flexible.

### Design Philosophy
Each pipeline step is designed to be **modular, scalable, and optimized for its task**, often requiring different compute environments or frameworks.
#### Key Reasons

##### 1. Modularity
Each step can use a different framework or script:
- Preprocessing: `scikit-learn`
- Training: `XGBoost`, `TensorFlow`, or `PyTorch`
- Evaluation: plain Python or custom logic

Each container is self-contained and runs independently.

##### 2. Optimized Compute Resources
Different steps often require different resources:
- **Processing**: CPU-heavy (e.g. `ml.m5.xlarge`)
- **Training**: GPU-heavy (e.g. `ml.p3.2xlarge`)
- **Evaluation**: Lightweight (e.g. `ml.t3.medium`)

Running everything on a single instance would be inefficient and expensive.

##### 3. Failure Isolation
Each step runs independently. If one fails:
- The pipeline can retry just that step
- You don’t need to rerun the entire workflow

This makes debugging and reliability much better.

##### 4. Caching & Reusability
SageMaker can **cache the results of completed steps**:
- Reuse them if input parameters haven't changed
- Skip unnecessary re-processing

This saves both time and cost.


##### 5. Parallelism
Steps that are not dependent on each other can:
- Run in parallel
- Improve total pipeline execution speed

#### 🧰 But Can I Combine Steps?
Yes, you can combine multiple logical steps into a single script if needed:



# Feature store

References: https://github.com/aws-samples/amazon-sagemaker-feature-store-examples/blob/main/Sagemaker-FeatureStore/01_hello/01_hello.ipynb
 
 - Amazon SageMaker Feature Store is a centralized repository for managing machine learning features.
 - It simplifies the process of data exploration, model training, and batch predictions by providing a unified view of your features.
 - Enhances ML model development and deployment efficiency.
 - Easy to share the features to others in team.
 - Data Lineage makes it easy to track origin


### Here are some common terms used in the Amazon SageMaker Feature Store:
 - Feature Store: A centralized repository for managing machine learning features, serving as the single source of truth for your data by storing, retrieving, removing, tracking, sharing, discovering, and controlling feature access.
 - Online Store: Provides real-time access to the latest feature data, enabling low-latency applications.
 - Offline Store: Stores historical feature data, often used for batch processing, offline analysis, or model training.
 - Feature Group: A collection of related features used to describe a set of records, serving as the foundation for training and predicting with machine learning models.
 - Feature: A property or characteristic used as input for machine learning models. In a Feature Store, a feature represents a column in your ML data table.
 - Feature Definition:  Specifies the name and data type (integral, string, or fractional) of a feature within a feature group.
 - Record:  A collection of feature values for a specific entity, uniquely identified by a combination of record identifier and event time. In a Feature Store, a record represents a row in your ML data table.
 - Record Identifier:  The name of the feature used to identify records within a feature group uniquely. It must be defined among the feature group’s feature definitions.
 - Event Time: A timestamp associated with a record event, indicating when the data was captured or updated. All records in a feature group must have an event time. The online store only stores the latest record for each entity, while the offline store retains all  -  - historical records.
 - Ingestion: The process of adding new records to a feature group, typically performed using the PutRecord API.


# How does Feature Store works?
i.e. where it stores the data, can we analyze data in featture store etc.
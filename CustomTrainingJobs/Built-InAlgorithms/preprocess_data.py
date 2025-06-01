
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from typing import List, Optional, Tuple

## Transform Columns i.e.
## 1. Fill Missings with "None" and Encode categorical features
## 2. Fill missing with -1 and Standardize numerical features

def preprocess_data_general_util(train: pd.DataFrame, test: pd.DataFrame, target: str, features: Optional[List[str]]=None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Takes train and test data fill in missings and transforms the features, i.e. OneHotEncoding, StandardScaler
    
    Parameters:
        train (pd.DataFrame): Training DataFrame
        test (pd.DataFrame): Testing DataFrame
        target (str): Name of the target column
        features (List[str], optional): List of feature column names. If None, all columns except target are used.
        
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]: X_train, X_test, y_train, y_test
    """
    if features == None:
        features = [col for col in train.columns if target not in col]
    else:
        train = train[features]
        test = test[features]
        
    numeric_features = train.select_dtypes(include=['number']).columns.tolist()
    categorical_features = train.select_dtypes(include=['object']).columns.tolist()
    print("Numeric Feature: ", numeric_features)
    print("Categoy Feature: ", categorical_features)
    
    # Pipelines for each type
    numeric_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value=-1)),
        ('scaler', StandardScaler())
    ])
    
    categorical_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='None')),
        ('encoder', OneHotEncoder(handle_unknown='ignore',sparse_output=False, drop='first'))
    ])
    
    preprocessor = ColumnTransformer(transformers=(
        ("num", numeric_pipeline, numeric_features),
        ("cat", categorical_pipeline, categorical_features)
    ))
    
    train2 = preprocessor.fit_transform(train)
    #test2 = preprocessor.fit_transform(test) # There is some issue in test processing so commentinf it for now
    
    # The above code will generate a numpy array, you need to assign names to encoded factors as below 
    encoder = preprocessor.named_transformers_['cat'].named_steps['encoder']
    cat_cols = encoder.get_feature_names_out(categorical_features)
    
    all_columns = list(numeric_features) + list(cat_cols)
    train2 = pd.DataFrame(train2, columns=all_columns)
    
    target = [col for col in all_columns if target in col]
    print(target)
    train2 = pd.concat([train2.pop(target[0]), train2], axis=1)
    #test = pd.concat([test.pop('Target'), test], axis=1)
    
    
    print(train.shape, test.shape)
    print(train2.shape)#, test2.shape)
    print(train2.columns)
    return train2, pd.DataFrame()
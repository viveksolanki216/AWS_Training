import os
import pandas as pd
import argparse
from sklearn.metrics import roc_auc_score
import json

if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description="Pre-Processes the data")
    #parser.add_argument("data-file-path", type='str', help="dataset")#, default="/opt/ml/processing/input/dataset.csv")

    # There are no dedicated channels for data pre-processing jobs       
    # Load the test data actual tareget
    test = pd.read_csv('/opt/ml/processing/test/test.csv')
    target = test.pop('fraud')
    
    # Load the predictions made by batch transform job
    predictions = pd.read_csv('/opt/ml/processing/test_predictions/test_to_predict.csv.out', header=None)
    predictions = predictions[predictions.columns[0]]
    
    test_auc = roc_auc_score(target.values, predictions.values)
    print("Area Under ROC Curve: ", round(test_auc,2))

    # Save metrics
    metrics = {
        "test-auc-mean": test_auc,
    }
    
    with open('/opt/ml/processing/evaluation/test_metrics.json', 'w') as f:
        json.dump(metrics, f)
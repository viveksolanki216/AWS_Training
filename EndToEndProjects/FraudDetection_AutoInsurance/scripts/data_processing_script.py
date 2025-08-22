    import os
import pandas as pd
import argparse

if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description="Pre-Processes the data")
    #parser.add_argument("data-file-path", type='str', help="dataset")#, default="/opt/ml/processing/input/dataset.csv")

    # There are no dedicated channels for data pre-processing jobs       
    dataset = pd.read_csv('/opt/ml/processing/input/dataset.csv')
    # Dropping the first colums which is row number that mistakenly added.
    dataset = dataset.iloc[:,1:]
    
    dataset_col_order = ['fraud']  + list(dataset.drop(["fraud", "policy_id"], axis=1).columns)
    train = dataset.sample(frac=.80, random_state=0)[dataset_col_order]
    test = dataset.drop(train.index)[dataset_col_order]


    train.to_csv("/opt/ml/processing/output/train.csv", index=False)
    test.to_csv("/opt/ml/processing/output/test.csv", index=False)

    # Drop target and headers from the test data for batch transform predictions. The api takes a s3 data uri to predict
    #test_data = pd.read_csv(test_data_s3_uri)
    target = test.pop('fraud')
    test.to_csv("/opt/ml/processing/output/test_to_predict.csv", index=False, header=False)

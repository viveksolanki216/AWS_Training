import os
import pandas as pd
import argparse

if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description="Pre-Processes the data")
    #parser.add_argument("data-file-path", type='str', help="dataset")#, default="/opt/ml/processing/input/dataset.csv")

    # There are no dedicated channels for data pre-processing jobs       
    dataset = pd.read_csv('/opt/ml/processing/input/dataset.csv')
    
    dataset_col_order = ['fraud']  + list(dataset.drop(["fraud", "policy_id"], axis=1).columns)
    train = dataset.sample(frac=.80, random_state=0)[dataset_col_order]
    test = dataset.drop(train.index)[dataset_col_order]
    
    train.to_csv("/opt/ml/processing/output/train.csv", index=False)
    test.to_csv("/opt/ml/processing/output/test.csv", index=False)
    
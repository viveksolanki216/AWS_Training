import os
import pandas as pd
import argparse
import xgboost as xgb
import pickle
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a model for fraud detection")
    parser.add_argument("--train-data-path",       type=str, default=os.environ.get("SM_CHANNEL_TRAIN"), help="Directory containing the training & testing data")
    parser.add_argument("--train-file",            type=str, default='train.csv', help="Directory containing the training & testing data")
    parser.add_argument("--test-data-path",        type=str, default=os.environ.get("SM_CHANNEL_TEST"), help="Directory containing the training & testing data")
    parser.add_argument("--test-file",             type=str, default='test.csv', help="Directory containing the training & testing data")
    parser.add_argument("--model-out-dir",         type=str, default=os.environ.get("SM_MODEL_DIR"), help="Directory to save the trained model")
    parser.add_argument("--model-data-out-dir",    type=str, default=os.environ.get("SM_OUTPUT_DATA_DIR"), help="Directory to save the trained model")
    parser.add_argument("--target-var",            type=str, default='fraud', help="Target variable for the model")
    parser.add_argument("--features",              type=str, default=None, help="| list of feature variables")
    parser.add_argument("--max-depth",             type=int, default=6, help="Maximum depth of the tree")
    parser.add_argument("--eta",                   type=float, default=0.3, help="Learning rate")
    parser.add_argument("--objective",             type=str, default="binary:logistic", help="Learning task and objective function.")
    parser.add_argument("--num-boost-round",       type=int, default=1, help="Number of boosting rounds")
    parser.add_argument("--nfold",                 type=int, default=2, help="Number of boosting rounds")

    print("Parsing arguments...")
    args = parser.parse_args()
    print(args)

    # Load the data

    # TRAIN
    print(args.train_file)
    print("Reading Train Data From", os.path.join(args.train_data_path, args.train_file))
    train = pd.read_csv(os.path.join(args.train_data_path, args.train_file))
    print(f"Training data shape: {train.shape}")
    for col in train.select_dtypes(include=['object']).columns:
        train[col] = pd.to_numeric(train[col], errors='coerce')
    #print(train.dtypes)

    #test = pd.read_csv(args.test_file)
    #print(f"Test data shape: {test.shape}")
    #for col in test.select_dtypes(include=['object']).columns:
    #    test[col] = pd.to_numeric(test[col], errors='coerce')
    #print(test.dtypes)
    
    #target = 'fraud'
    target = args.target_var
    train_target = train.pop(target)
    #test_target = test.pop(target)

    if args.features == None:
        features = train.columns.tolist()
    else:
        features = args.features.split('|')

    # conver data to DMatrix
    dtrain = xgb.DMatrix(train[features], label=train_target)

    hyper_params = {"max_depth": args.max_depth, "eta": args.eta, "objective": args.objective}
    # Cross validation
    cv_results = xgb.cv(
        params=hyper_params,
        dtrain=dtrain,
        num_boost_round=args.num_boost_round,
        nfold=args.nfold,
        metrics="auc",
        seed=42,
        early_stopping_rounds=10,
    )

    
    print(f"[0]#011train-auc:{cv_results.iloc[-1]['train-auc-mean']}")
    # print(f"[1]#011train-auc std:{cv_results.iloc[-1]['train-auc-std']}")
    print(f"[1]#011validation-auc:{cv_results.iloc[-1]['test-auc-mean']}")
    # print(f"[1]#011validation-auc std:{cv_results.iloc[-1]['test-auc-std']}")

    metrics_data = {
        "binary_classification_metrics": {
            "validation:auc": {
                "value": cv_results.iloc[-1]["test-auc-mean"],
                "standard_deviation": cv_results.iloc[-1]["test-auc-std"]
            },
            "train:auc": {
                "value": cv_results.iloc[-1]["train-auc-mean"],
                "standard_deviation": cv_results.iloc[-1]["train-auc-std"]
            },
        }
    }

    model = xgb.train(params=hyper_params, dtrain=dtrain, num_boost_round=len(cv_results))
    print("model training done")
    # Save the model to the location specified by ``model_dir``
    metrics_location = args.model_data_out_dir + "/metrics.json"
    model_location = args.model_out_dir + "/xgboost-model"

    with open(metrics_location, "w") as f:
        json.dump(metrics_data, f)

    with open(model_location, "wb") as f:
        pickle.dump(model, f)
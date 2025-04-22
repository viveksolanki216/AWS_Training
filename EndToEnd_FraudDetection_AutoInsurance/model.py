import os
import pandas as pd
import argparse
import xgboost as xgb

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a model for fraud detection.")
    parser.add_argument("--data-dir", type=str, default='data/', help="Directory containing the training & testing data.")
    parser.add_argument("--model-out-dir", type=str, required=True, help="Directory to save the trained model.")
    parser.add_argument("--target-var", type=str, default='fraud', help="Target variable for the model.")
    parser.add_argument("--features", type=str, default=None, help="| list of feature variables.")
    parser.add_argument("--max-depth", type=int, default=6, help="Maximum depth of the tree.")
    parser.add_argument("--eta", type=float, default=0.3, help="Learning rate.")
    parser.add_argument("--objective", type=str, default="binary:logistic", help="Learning task and objective function.")

    print("Parsing arguments...")
    args = parser.parse_args()
    print(args)
    print(args.data_dir)
    print(args.model_out_dir)
    print(args.target_var)
    print(args.features)

    # Load the data

    # TRAIN
    data_dir = args.data_dir
    #data_dir = "EndToEnd_FraudDetection_AutoInsurance/data"
    train = pd.concat([
        pd.read_csv(os.path.join(data_dir, file))
        for file in os.listdir(data_dir)
        if 'train' in file
    ])
    print(f"Training data shape: {train.shape}")

    test = pd.concat([
        pd.read_csv(os.path.join(data_dir, file))
        for file in os.listdir(data_dir)
        if 'test' in file
    ])
    print(f"Test data shape: {test.shape}")

    #target = 'fraud'
    target = args.target_var
    train_target = train.pop(target)
    test_target = test.pop(target)

    if features == None:
        features = train.columns.tolist()
    else:
        features = args.features.split('|')

    # conver data to DMatrix
    dtrain = xgb.DMatrix(train[features], label=train_target)

    hyper_params = {"max_depth": args.max_depth, "eta": args.eta, "objective": args.objective}
    # Cross validation
    cv_results = xgboost.cv(
        params=hyper_params,
        dtrain=dtrain,
        num_boost_round=100,
        nfold=5,
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

    model = xgb.train(params=params, dtrain=dtrain, num_boost_round=len(cv_results))

    # Save the model to the location specified by ``model_dir``
    metrics_location = args.output_data_dir + "/metrics.json"
    model_location = args.model_dir + "/xgboost-model"

    with open(metrics_location, "w") as f:
        json.dump(metrics_data, f)

    with open(model_location, "wb") as f:
        pickle.dump(model, f)
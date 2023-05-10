# artifacts\raw_local_dir\data.csv

import argparse
import os
import pandas as pd
import logging
from src.utils.common import read_yaml, create_directories,save_json
import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np


STAGE = "MODEL_EVALUATION" 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )

def evaluate_metrics(actual_values, predicted_values):
    rmse = np.sqrt(mean_squared_error(actual_values, predicted_values))
    mae = mean_absolute_error(actual_values, predicted_values)
    r2 = r2_score(actual_values, predicted_values)
    return rmse, mae, r2

def evaluate_model(config_path,param_path):
    ## read config files
    logging.info(f"Reading the config file from path={config_path}")
    config = read_yaml(config_path)
    logging.info(f"Config file read successfully\n The config file contains\n {config}")
    logging.info(f"Reading the param file from path={param_path}")
    param = read_yaml(param_path)
    logging.info(f"Param file read successfully\n The param file contains\n {param}")
    
    
    artifact_dir = config['artifacts']['ARTIFACTS_DIR']

    model_dir = config['artifacts']['TRAIN_MODEL_DIR']
    create_directories([os.path.join(artifact_dir,model_dir)])
    model_filename= config["artifacts"]['TRAIN_MODEL_FILENAME']
    model_path = os.path.join(artifact_dir,model_dir,model_filename)

    lr = joblib.load(model_path)
    logging.info(f" {model_path} has been succesfully loaded")
    
    split_dir = config['artifacts']['SPLIT_DIR']   

    test_filename= config['artifacts']['TEST_FILE']

    test_path = os.path.join(artifact_dir,split_dir,test_filename)
    logging.info(f"The train file path is {test_path}")

    test_df = pd.read_csv(test_path)
    logging.info(f"Dataframe has {test_df.shape[0]} rows\n no of columns ={test_df.shape[1]}")
    
    target_column = param['model_params']['target_column']
    X_test = test_df.drop(target_column,axis=1)
    y_test = test_df[target_column]

    predicted_values = lr.predict(X_test)

    rmse, mae, r2 = evaluate_metrics(y_test, predicted_values)

    scores_dir = config['artifacts']['REPORTS_DIR']
    create_directories([os.path.join(artifact_dir,scores_dir)])

    report_filenam = config['artifacts']['SCORES_FILENAME']
    report_path = os.path.join(artifact_dir,scores_dir,report_filenam)

    scores ={
        "rmse": rmse,
        "mae": mae,
        "r2": r2
    }
    save_json(path=report_path,data=scores)

    
if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params","-p",default="params.yaml")
    parsed_args = args.parse_args()
    # print(parsed_args)
    
    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        logging.info(f"Config path = {parsed_args.config}")
        logging.info(f"Param path = {parsed_args.params}")
        evaluate_model(config_path=parsed_args.config,param_path=parsed_args.params)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e
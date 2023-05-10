# artifacts\raw_local_dir\data.csv

import argparse
import os
import pandas as pd
import logging
from src.utils.common import read_yaml, create_directories
from sklearn.linear_model import ElasticNet
import joblib


STAGE = "MODEL_TRAINING" 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def train_data(config_path,param_path):
    ## read config files
    logging.info(f"Reading the config file from path={config_path}")
    config = read_yaml(config_path)
    logging.info(f"Config file read successfully\n The config file contains\n {config}")
    logging.info(f"Reading the param file from path={param_path}")
    param = read_yaml(param_path)
    logging.info(f"Param file read successfully\n The param file contains\n {param}")
    
    artifact_dir = config['artifacts']['ARTIFACTS_DIR']

    split_dir = config['artifacts']['SPLIT_DIR']   

    train_filename= config['artifacts']['TRAIN_FILE']

    train_path = os.path.join(artifact_dir,split_dir,train_filename)
    logging.info(f"The train file path is {train_path}")

    train_df = pd.read_csv(train_path)
    logging.info(f"Dataframe has {train_df.shape[0]} rows\n no of columns ={train_df.shape[1]}")
    
    target_column = param['model_params']['target_column']
    X_train = train_df.drop(target_column,axis=1)
    y_train = train_df[target_column]

    alpha = param['model_params']['ElasticNet_params']['alpha']
    l1_ratio = param['model_params']['ElasticNet_params']['l1_ratio']
    random_state = param['base']['random_state']

    lr = ElasticNet(alpha=alpha,l1_ratio=l1_ratio,random_state=random_state)
    lr.fit(X_train,y_train)

    model_dir = config['artifacts']['TRAIN_MODEL_DIR']
    create_directories([os.path.join(artifact_dir,model_dir)])
    model_filename= config["artifacts"]['TRAIN_MODEL_FILENAME']
    model_path = os.path.join(artifact_dir,model_dir,model_filename)

    joblib.dump(lr,model_path)
    logging.info(f"{model_filename} has been dumped at {model_path}")
    
    
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
        train_data(config_path=parsed_args.config,param_path=parsed_args.params)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e
# artifacts\raw_local_dir\data.csv

import argparse
import os
import pandas as pd
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories,save_file
from sklearn.model_selection import train_test_split
# import random


STAGE = "DATA_VALIDATION" 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def split_data(config_path,param_path):
    ## read config files
    logging.info(f"Reading the config file from path={config_path}")
    config = read_yaml(config_path)
    logging.info(f"Config file read successfully\n The config file contains\n {config}")
    logging.info(f"Reading the param file from path={param_path}")
    param = read_yaml(param_path)
    logging.info(f"Param file read successfully\n The param file contains\n {param}")
    
    artifact_dir = config['artifacts']['ARTIFACTS_DIR']
    raw_local_dir = config['artifacts']['RAW_LOCAL_DIR']
    raw_local_file = config['artifacts']['RAW_LOCAL_FILE']
    
    file_path = os.path.join(artifact_dir,raw_local_dir,raw_local_file)
    logging.info(f"The data is present in {file_path} location")
    df = pd.read_csv(file_path)
    logging.info(f'Dataframe read successfully\n The shape of dataframe is {df.shape}')
    print(df.head(3)) 

    test_size = param['base']['test_size']
    random_state = param['base']['random_state']

    train,test = train_test_split(df,test_size=test_size,random_state=random_state)

    split_dir = config['artifacts']['SPLIT_DIR']
    create_directories([os.path.join(artifact_dir,split_dir)])
    
    train_filename= config['artifacts']['TRAIN_FILE']
    test_filename = config['artifacts']['TEST_FILE']

    train_path = os.path.join(artifact_dir,split_dir,train_filename)
    logging.info(f"The train file path is {train_path}")
    test_path = os.path.join(artifact_dir,split_dir,test_filename)
    logging.info(f"The train file path is {test_path}")

    for data,data_path in (train,train_path),(test,test_path):
        save_file(dataframe=data,path=data_path)
    logging.info(f"Both Train and Test files have been succesully done.")
    


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
        split_data(config_path=parsed_args.config,param_path=parsed_args.params)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e
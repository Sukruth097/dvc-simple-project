import argparse
import os
import pandas as pd
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
# import random


STAGE = "DATA_INGESTION" 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def get_data(config_path):
    ## read config files
    logging.info(f"Reading the config file from path={config_path}")
    config = read_yaml(config_path)
    logging.info(f"Config file read successfully\n The config file contains\n {config}")
    # print(config)
    data_path= config['datasource']
    logging.info(f"The data file is = {data_path}")
    df = pd.read_csv(data_path,sep=';')
    logging.info(f'Dataframe read successfully\n The shape of dataframe is {df.shape}')
    print(df.head(3))   
    artifact_dir = config['artifacts']['ARTIFACTS_DIR']
    raw_local_dir = config['artifacts']['RAW_LOCAL_DIR']
    raw_local_file = config['artifacts']['RAW_LOCAL_FILE']

    raw_dir = os.path.join(artifact_dir,raw_local_dir)
    logging.info(f" The directories need to be created {raw_dir}")
    create_directories(path_to_directories=[raw_dir])
    raw_file = os.path.join(raw_dir,raw_local_file)
    logging.info(f"The raw file path where dataframe will be stored in {raw_file}")
    df.to_csv(raw_file, sep=',',index=False)
    logging.info(f"The csv file is succesfully dumped in {raw_file}")



if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    
    parsed_args = args.parse_args()
    # print(parsed_args)

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        get_data(config_path=parsed_args.config)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e
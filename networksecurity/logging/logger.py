import logging
import os
from datetime import datetime

LOG_FILE_FORMAT = f"{datetime.now().strftime('%d_%m_%y_%H_%M_%S')}.log"
log_path = os.path.join(os.getcwd(),"logs",f"{datetime.now().strftime('%d_%m_%y_%H_%M_%S')}")

os.makedirs(log_path,exist_ok=True)

logs_file_path = os.path.join(log_path,LOG_FILE_FORMAT)

logging.basicConfig(
    filename=logs_file_path,
    level=logging.INFO,
    format= "%(asctime)s-%(levelname)s-%(message)s"
)

import yaml
import pandas as pd
import pyarrow.dataset as ds
from os import path

def load_config(path):
  """ Parse only basic/trusted tags in a YAML config file and 
  produce the corresponding Python object.
  
  Arguments:
    path: path to config file
  
  Returns:
    An object (usually dict) containing parameters from the config file
  """
  with open(path, "r") as f:
    return yaml.safe_load(f)

config = load_config(path="config.yml")

fpath = config["python"]["participants_csv_path"]

f = pd.read_csv(fpath, engine="pyarrow")

participant_ids = list(set(f["PARTICIPANT_ID"].tolist()))

source_dataset_path = config["python"]["source_dataset_path"]

dataset = ds.dataset(source=source_dataset_path)

# participant_ids.extend([path.basename(path.dirname(x)) for x in dataset.files][1:3])
selected_id_dirs = [x for x in dataset.files if path.basename(path.dirname(x)) in participant_ids]

filtered_dataset = ds.dataset(source=selected_id_dirs)

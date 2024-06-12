import yaml
import pandas as pd
import pyarrow.dataset as ds
from os import path

with open("config.yml", "r") as f:
  config = yaml.safe_load(f)

fpath = config["python"]["participants_csv_path"]

f = pd.read_csv(fpath, engine="pyarrow")

participant_ids = list(set(f["PARTICIPANT_ID"].tolist()))

source_dataset_path = config["python"]["source_dataset_path"]

dataset = ds.dataset(source=source_dataset_path)

# participant_ids.extend([path.basename(path.dirname(x)) for x in dataset.files][1:3])
selected_id_dirs = [x for x in dataset.files if path.basename(path.dirname(x)) in participant_ids]

filtered_dataset = ds.dataset(source=selected_id_dirs)

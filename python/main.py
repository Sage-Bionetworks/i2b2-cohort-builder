import yaml
import pandas as pd
import os

with open("config.yml", "r") as f:
  config = yaml.safe_load(f)

fpath = config["python"]["participants_csv_path"]

f = pd.read_csv(fpath, engine="pyarrow")

participant_ids = list(set(f["PARTICIPANT_ID"].tolist()))

source_dataset_path = config["python"]["source_dataset_path"]

participant_partitions = []
for r,d,_ in os.walk(source_dataset_path):
  for dir in d:
    participant_partitions.append(os.path.join(r,dir))

selected_id_dirs = [dir for dir in participant_partitions if os.path.basename(dir) in participant_ids]

destination_dataset_path = config["python"]["destination_dataset_path"]

# os.makedirs(os.path.join(destination_dataset_path, os.path.basename(source_dataset_path)))

for dir in participant_partitions:
  if os.path.basename(dir) not in participant_ids:
    print(False)

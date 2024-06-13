import yaml
import pandas as pd
import pyarrow.dataset as ds
from os import path

def load_config(path):
  """
  Parse only basic/trusted tags in a YAML config file and produce the 
  corresponding Python object.
  
  Arguments:
    path: path to config file
  
  Returns:
    An object (usually dict) containing parameters from the config file
  """
  with open(path, "r") as f:
    return yaml.safe_load(f)

def get_cohort_partition_paths(selected_participants_manifest_path, source_dataset_path):
  """
  Get a list of Participant Identifiers to extract data for from a dataset that 
  is partitioned by Participant Identifier
  
  Arguments:
    selected_participants_manifest_path: path to manifest file containing 
      selected Participant Identifiers
    source_dataset_path: path to participant-partitioned dataset we want to 
      extract participant-partitions from
  
  Returns:
    A list containing the unique Participant Identifiers that are in our 
    manifest list of selected participants and in our source dataset
  """
  f = pd.read_csv(selected_participants_manifest_path, engine="pyarrow")
  
  participant_ids = list(set(f["PARTICIPANT_ID"].tolist()))
  
  dataset = ds.dataset(source=source_dataset_path)
  
  selected_id_dirs = [x for x in dataset.files if path.basename(path.dirname(x)) in participant_ids]
  
  return selected_id_dirs

def build_cohort(selected_partitions_list):
  """
  Extract partitions from a dataset that is partitioned by Participant 
  Identifier given a list of paths to Participant Identifier partitions from 
  the original dataset
  
  Arguments:
    selected_partitions_list: A list of paths pointing to dataset partitions
  
  Returns:
    A pyarrow Dataset object
  """
  filtered_dataset = ds.dataset(source=selected_partitions_list)
  
  return filtered_dataset

if __name__ == "__main__":
  config = load_config(path="config.yml")
  
  selected_id_dirs = get_cohort_partition_paths(
    selected_participants_manifest_path=config["python"]["participants_csv_path"],
    source_dataset_path=config["python"]["source_dataset_path"])
  
  filtered_dataset = build_cohort(selected_id_dirs)


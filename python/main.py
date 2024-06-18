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


def get_cohort_partition_paths(manifest_path, dataset_path):
    """
    Get a list of Participant Identifiers to extract data for from a dataset
    that is partitioned by Participant Identifier

    Arguments:
        manifest_path: path to manifest file containing selected
        Participant Identifiers
        dataset_path: path to participant-partitioned dataset to
        extract participant-partitions from

    Returns:
        A list containing the unique Participant Identifiers that are in our
        manifest list of selected participants and in our source dataset
    """
    f = pd.read_csv(selected_participants_manifest_path, engine="pyarrow")

    participant_ids = list(set(f["PARTICIPANT_ID"].tolist()))

    dataset = ds.dataset(source=source_dataset_path)

    selected_id_dirs = [
        file for file in dataset.files
        if path.basename(path.dirname(file)) in participant_ids]

    return selected_id_dirs


def build_cohort(partition_paths):
    """
    Extract partitions from a dataset that is partitioned by Participant
    Identifier given a list of paths to Participant Identifier partitions from
    the original dataset

    Arguments:
        partition_paths: A list of paths pointing to dataset partitions

    Returns:
        A pyarrow Dataset object
    """
    filtered_dataset = ds.dataset(source=partition_paths)

    return filtered_dataset


if __name__ == "__main__":
    config = load_config(
        path="config.yml"
    )

    selected_id_dirs = get_cohort_partition_paths(
        manifest_path=config["python"]["participants_csv_path"],
        dataset_path=config["python"]["source_dataset_path"]
    )

    filtered_dataset = build_cohort(
        partition_paths=selected_id_dirs
    )


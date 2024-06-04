import pandas as pd

fpath = "participant_ids.csv"

f = pd.read_csv(fpath, engine="pyarrow")

participant_ids = list(set(f["PARTICIPANT_ID"].tolist()))

# get list of datasets
# for dataset in datasets_dir:
  # temp_df = dataset.filter(ParticipantIdentifier in participant_ids)
  # temp_df.write(format, output_dir)

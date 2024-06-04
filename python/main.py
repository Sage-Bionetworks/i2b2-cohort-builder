import pandas as pd

fpath = "participant_ids.csv"

f = pd.read_csv(fpath, engine="pyarrow")

participant_ids = list(set(f["PARTICIPANT_ID"].tolist()))

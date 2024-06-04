import pandas as pd

fpath = "/path/to/csv"

f = pd.read_csv(fpath, engine="pyarrow")

participant_ids = f["ParticipantIdentifier"].tolist()

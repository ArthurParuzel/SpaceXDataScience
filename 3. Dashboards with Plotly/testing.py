import pandas as pd
from pathlib import Path

file = Path("C:\HomeCloud\Learning Dropbox\IBM\Data Science\Applied Data Science Capstone\Week 3\spacex_launch_dash.csv")
spacex_df = pd.read_csv(file)


select_site = spacex_df.loc[spacex_df['Launch Site'] == 'CCAFS LC-40']     


success_failure_df = select_site.groupby('class').size().reset_index(name='class count')
colnames = ["result","count"]
success_failure_df.columns = colnames

col3 = []
for index,row in success_failure_df.iterrows():
    if row["result"] == 0:
        col3.append("Failure")
    else:
        col3.append("Success")
        
success_failure_df["result text"] = col3

print(success_failure_df)

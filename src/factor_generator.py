import pandas as pd
from pathlib import Path

#create path to retrieve ticker data from data folder
project_root = Path(__file__).parent.parent
data_folder = project_root / "data"
raw_folder = project_root / "data" / "raw"
factors_folder = project_root / "data" / "factors"



#create dataframe to read csv data
df = pd.read_csv(raw_folder / "AAPL.csv")

#calculate 30 and 90 day moment --> end/start - 1
df["momentum_30"] = (df["Close"] / df["Close"].shift(30)) - 1
df["momentum_90"] = (df["Close"] / df["Close"].shift(90)) - 1

#calculate volatility by std dev of 1 day momentum over X day time span
one_day_momentums = (df["Close"] / df["Close"].shift(1)) - 1
df["volatility_30"] = one_day_momentums.rolling(30).std()
df["volatility_90"] = one_day_momentums.rolling(90).std()


momentum_df = df[[
    "Date",
    "momentum_30",
    "momentum_90",
    "volatility_30",
    "volatility_90",
]]


momentum_df.to_csv(factors_folder / "AAPL_factors.csv", index = False)
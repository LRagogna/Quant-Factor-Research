import pandas as pd
from pathlib import Path

#create path to retrieve ticker data from data folder
project_root = Path(__file__).parent.parent
data_folder = project_root / "data"
raw_folder = project_root / "data" / "raw"
factors_folder = project_root / "data" / "factors"


def get_factors(df):
    #calculate 30 and 90 day moment --> end/start - 1
    df["momentum_30"] = (df["Close"] / df["Close"].shift(30)) - 1
    df["momentum_90"] = (df["Close"] / df["Close"].shift(90)) - 1

    #calculate volatility by std dev of 1 day momentum over X day time span
    one_day_momentums = (df["Close"] / df["Close"].shift(1)) - 1
    df["volatility_30"] = one_day_momentums.rolling(30).std()
    df["volatility_90"] = one_day_momentums.rolling(90).std()

    #calculate moving average distance (how far stock moves from average over X day time span, relative percentage)
    df["moving_average_30"] = df["Close"] / df["Close"].rolling(30).mean() - 1
    df["moving_average_90"] = df["Close"] / df["Close"].rolling(90).mean() - 1

    #calculate volume ratio (relative percentage) of X day time span 
    df["volume_ratio_30"] = df["Volume"] / df["Volume"].rolling(30).mean() - 1
    df["volume_ratio_90"] = df["Volume"] / df["Volume"].rolling(90).mean() - 1

    return df[[
        "Date",
        "momentum_30",
        "momentum_90",
        "volatility_30",
        "volatility_90",
        "moving_average_30",
        "moving_average_90",
        "volume_ratio_30",
        "volume_ratio_90"
    ]]


'''
create dataframe to read csv data for each data file in raw_folder
'''
for file in raw_folder.glob("*.csv"):
    symbol = file.stem
    df = pd.read_csv(file)
    factor_df = get_factors(df)

    factor_df.to_csv(factors_folder / f"{symbol}_factors.csv", index = False)
import pandas as pd


def calculate_average_time_per_user(df: pd.DataFrame):
    df.dropna(inplace=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    time_spent_per_user = df.groupby(['user_id']).size().reset_index(name='Time Spent (in seconds)')
    unique_flyer_per_user = df.groupby(['user_id'])["flyer_id"].unique().apply(len).reset_index(name='unique_flyers')
    result = pd.merge(time_spent_per_user, unique_flyer_per_user, on='user_id')
    result["Avg. Time spent in seconds"] = result["Time Spent (in seconds)"] / result["unique_flyers"]
    print(result.head())

    return result

import warnings
import pandas as pd
from analysis import Analysis

warnings.filterwarnings(action='ignore')


class Reporting:

    def __init__(self):
        pass

    def clean(self, df: pd.DataFrame):
        # convert timestamp column to timestamp type from string type
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        #  Filling in the missing merchant_id column value based on the flyer_id
        df2 = df[["flyer_id", "merchant_id"]]
        df2.dropna(inplace=True)
        for merchant_id in df2["merchant_id"].unique():
            df.loc[df['flyer_id'].isin(df2[df2["merchant_id"] == merchant_id]["flyer_id"].unique())][
                "merchant_id"] = merchant_id

        return df

    def generate_report(self, csv_file_path: str):
        df = pd.read_csv(csv_file_path)
        df = self.clean(df)

        for merchant_id in df['merchant_id'].dropna().head().unique():
            merchant_df = df[df["merchant_id"] == merchant_id]
            analysis_obj = Analysis()
            analysis_obj.analyse(merchant_id, merchant_df)


if __name__ == "__main__":
    Reporting().generate_report("./Data Engineer Take home dataset - dataset.csv")

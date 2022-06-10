import pandas as pd
import matplotlib.pyplot as plt
import os
from plot import Plotting


class Analysis:

    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        if not os.path.exists(f"{self.path}/plottings"):
            os.mkdir(f"{self.path}/plottings/")

    def plot_event_distribution(self, merchant_id: str, df: pd.DataFrame):
        if not df.empty:
            merchant = df[df["merchant_id"] == merchant_id]

            analysis = merchant.groupby("event").size().reset_index(name='Count')
            analysis.sort_values('Count', inplace=True, ascending=False)
            ax = analysis.set_index("event").plot(kind="bar", legend=True)
            for p in ax.patches:
                ax.annotate(str(p.get_height()), (p.get_x(), p.get_height()))

            fig = ax.get_figure()

            bar_graph_image_url = f'{self.path}/plottings/{merchant_id}_bar.png'
            fig.savefig(bar_graph_image_url)
            return bar_graph_image_url

    def find_best_worst_performing_flyer(self, merchant_id, df):
        agg_result = df[df["merchant_id"] == merchant_id].groupby("flyer_id").size().reset_index(name='Count')
        if not agg_result.empty:
            min_flyer_count_series = agg_result.loc[agg_result['Count'].idxmin()]
            max_flyer_count_series = agg_result.loc[agg_result['Count'].idxmax()]

            return {"best": max_flyer_count_series.to_dict(), "worst": min_flyer_count_series.to_dict()}

        return {"best": {"flyer_id": "NA", "Count": "NA"}, "worst": {"flyer_id": "NA", "Count": "NA"}}

    def find_hourly_distribution(self, merchant_id, df):
        merchant = df.groupby(df["timestamp"].dt.hour).size().reset_index(name='Count')
        ax = merchant.plot(x='timestamp', y='Count', kind='line', title='Hourly distribution of events occured')
        ax.set_xlabel('Hours')
        ax.set_ylabel('Number of events')
        plt.xticks(merchant['timestamp'])

        fig = ax.get_figure()
        line_graph_image_url = f'{self.path}/plottings/{merchant_id}_line.png'
        fig.savefig(line_graph_image_url)
        return line_graph_image_url

    def analyse(self, merchant_id, df):
        count_analysis = self.find_best_worst_performing_flyer(merchant_id, df)
        line_graph_image_url = self.find_hourly_distribution(merchant_id, df)
        bar_graph_image_url = self.plot_event_distribution(merchant_id, df)

        response = {
            'bar_graph_image_url': bar_graph_image_url,
            'line_graph_image_url': line_graph_image_url,
        }
        response.update(count_analysis)
        # print(response)
        Plotting().plot(merchant_id, response)
        return response

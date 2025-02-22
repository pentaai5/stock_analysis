from StrategyTester import StrategyTester
import numpy as np
import pandas as pd
import sys
import plotly.graph_objects as go 
import warnings
from plotly.subplots import make_subplots
from itertools import product
warnings.filterwarnings('ignore')

class BollingerBandTester (StrategyTester):
    def __init__(self):
        self.cmd_line = "python BollingerBandTester name='stock_name' start='YYYY-MM-DD' end='YYYY-MM-DD' long_only='True/False'"
        self.strategy_name = "Bollinger Band"


    def initialize(self):
        self.verifyParams()
        self.prepare_financial_data()
        self.short = 0 if self.context["long_only"] == "True" else -1

    def run_Strategy(self,window):
        self.data["SMA"] = self.data["Adj Close"].rolling(window).mean()
        self.data["STDDEV"] = self.data["Adj Close"].rolling(window).std()
        self.data["LOWER"] = self.data["SMA"] - 2*self.data["STDDEV"]
        self.data["UPPER"] = self.data["SMA"] + 2*self.data["STDDEV"]
        self.data["position"] = np.where( (self.data['Adj Close'].shift(2) > self.data['LOWER'].shift(2)) &
                                        (self.data['Adj Close'].shift(1) < self.data['LOWER'].shift(1)),1,
                            np.where((self.data['Adj Close'].shift(2) < self.data['UPPER'].shift(2)) &
                                        (self.data['Adj Close'].shift(1) > self.data['UPPER'].shift(1)),self.short,np.nan
                                    ) 
                            )
        self.data["position"].ffill(inplace=True)
        self.data["Strategy_returns"] = self.data["daily_returns"]*self.data["position"]
    
    def plot_data_curve(self):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace( go.Scatter(y=self.data["LOWER"],x=self.data.index,name="lower_band"),secondary_y=False)
        fig.add_trace( go.Scatter(y=self.data["UPPER"],x=self.data.index,name="upper_band"),secondary_y=False)
        fig.add_trace( go.Scatter(y=self.data["Adj Close"],x=self.data.index,name="Adj Close"),secondary_y=False)
        fig.add_trace( go.Scatter(y=self.data["position"],x=self.data.index,name="position"),secondary_y=True)
        fig.layout.update(title=self.strategy_name)
        fig.show(block=True)
    
    def optimise_Strategy(self,windowList):
        self.result = pd.DataFrame(columns=["Window","Strategy_returns","daily_returns"])
        for window in windowList:
            self.run_Strategy(window)
            df  = self.data[["Strategy_returns","daily_returns"]].cumsum().apply(np.exp)[-1:]
            if (len(df.index) == 1):
                self.result = pd.concat([self.result, 
                        pd.DataFrame([[window, df.iloc[0][0], df.iloc[0][1]]], 
                                    columns=["Window", "Strategy_returns", "daily_returns"])], 
                        ignore_index=True)

if __name__ == "__main__":
    s = BollingerBandTester()
    s.parse_and_initialize(sys.argv)
    windowList = [i for i in range(10,210,10)]
    s.optimise_Strategy(windowList)
    s.result.sort_values(by=['Strategy_returns'],ascending=False,inplace=True)
    print(s.result.head())
    s.run_Strategy(s.result.iloc[0][0])
    s.plot_data_curve()
    s.plot_performance_stats()

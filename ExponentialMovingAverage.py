from StrategyTester import StrategyTester
import numpy as np
import pandas as pd
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
from itertools import product
import sys

class ExponentialMovingAverageTester(StrategyTester):
    def __init__(self):
        self.cmd_line = "python ExponentialMovingAverageTester name='stock_name' start='YYYY-MM-DD' end='YYYY-MM-DD' long_only='True/False'"
        self.strategy_name = "Exponential Moving Average"
        

    def run_Strategy(self,window):
        self.data["EMA"] = self.data["Close"].ewm(span=window,adjust=False).mean()
        self.data["position"] = np.where( self.data["Close"].shift(1) >= self.data["EMA"].shift(1),1,
                                        np.where(self.data["Close"].shift(1) < self.data["EMA"].shift(1),self.short,np.nan))
        self.data["position"].ffill(inplace=True)
        self.data["Strategy_returns"] = self.data["daily_returns"]*self.data["position"]
    
    def plot_data_curve(self):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace( go.Scatter(y=self.data["EMA"],x=self.data.index,name="EMA"),secondary_y=False)
        fig.add_trace( go.Scatter(y=self.data["Close"],x=self.data.index,name="Close"),secondary_y=False)
        fig.add_trace( go.Scatter(y=self.data["position"],x=self.data.index,name="position"),secondary_y=True)
        fig.show(block=True)

        
    def optimise_Strategy(self,windowlist):
        self.result = pd.DataFrame(columns=["EMA","Strategy_returns","daily_returns"])
        for window in windowlist:
            self.run_Strategy(window)
            df  = self.data[["Strategy_returns","daily_returns"]].cumsum().apply(np.exp)[-1:]
            if (len(df.index) == 1):
                self.result = pd.concat([self.result, 
                        pd.DataFrame([[window, df.iloc[0][0], df.iloc[0][1]]], 
                                    columns=["EMA", "Strategy_returns", "daily_returns"])], 
                        ignore_index=True)
    


if __name__ == "__main__":
    s = ExponentialMovingAverageTester()
    s.parse_and_initialize(sys.argv)
    windowList = [i for i in range(10,210,10)]
    s.optimise_Strategy(windowList)
    s.result.sort_values(by=['Strategy_returns'],ascending=False,inplace=True)
    print(s.result.head())
    s.run_Strategy(s.result.iloc[0][0])
    s.plot_data_curve()
    s.plot_performance_stats()

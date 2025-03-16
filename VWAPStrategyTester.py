from StrategyTester import StrategyTester
import numpy as np
import pandas as pd
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
from itertools import product
import sys

class VWAPStrategyTester(StrategyTester):
    def __init__(self):
        self.cmd_line = "python VWAPStrategyTester name='stock_name' start='YYYY-MM-DD' end='YYYY-MM-DD' long_only='True/False'"
        self.strategy_name = "Rolling VWAP Strategy"
        
    def run_Strategy(self,window):
        self.data["Average_price"] = (self.data["Close"] + self.data["High"] + self.data["Low"])/3
        self.data["Weighted_Volume"] = self.data["Volume"]*self.data["Average_price"]
        self.data["VWAP"] = self.data["Weighted_Volume"].rolling(window).sum()/self.data["Volume"].rolling(window).sum()
        self.data["position"] = np.where( self.data["Close"].shift(1) <= self.data["VWAP"].shift(1),1,
                                        np.where(self.data["Close"].shift(1) > self.data["VWAP"].shift(1),self.short,np.nan)
                                        )
        self.data["position"].ffill()
        self.data["Strategy_returns"]=self.data["daily_returns"]*self.data["position"]
    
    def plot_data_curve(self):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace( go.Scatter(y=self.data["VWAP"],x=self.data.index,name="VWAP"),secondary_y=False)
        fig.add_trace( go.Scatter(y=self.data["Close"],x=self.data.index,name="Close"),secondary_y=False)
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
            if (window == 10) : 
                print(self.data.head(100))

if __name__ == "__main__":
    s = VWAPStrategyTester()
    s.parse_and_initialize(sys.argv)
    windowList = [i for i in range(10,100,10)]
    s.optimise_Strategy(windowList)
    s.result.sort_values(by=['Strategy_returns'],ascending=False,inplace=True)
    print(s.result.head())
    s.run_Strategy(s.result.iloc[0][0])
    s.plot_data_curve()
    s.plot_performance_stats()
